import os
import time
import urllib.parse
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import date, timedelta
from dotenv import load_dotenv
from prescription_reader import read_prescription_image
from medicine_tracker import track_medicines
from alert_system import send_medicine_alert
from reminder_poster import create_medicine_poster
from weekly_report import send_weekly_report
from reorder_system import send_reorder_alert

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs('uploads', exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        patient_name = request.form.get('patient_name', 'Patient')
        caregiver_email = request.form.get('caregiver_email', '')
        location = request.form.get('location', 'Ernakulam, Kerala')

        tablets = {
            'dpearl': int(request.form.get('dpearl', 8)),
            'cetirizine': int(request.form.get('cetirizine', 5)),
            'omeprazole': int(request.form.get('omeprazole', 5)),
        }

        # ─────────────────────────────────────────
        # STEP 1: Save uploaded prescription image
        # ─────────────────────────────────────────
        file = request.files['prescription']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # ─────────────────────────────────────────
        # STEP 2: Read prescription with AI
        # ─────────────────────────────────────────
        prescription_result = read_prescription_image(filepath)
        time.sleep(2)

        # ─────────────────────────────────────────
        # STEP 3: Build medicines list
        # ─────────────────────────────────────────
        medicines = [
            {
                'name': 'Cap. D-Pearl 60k',
                'tablets_per_day': 1,
                'timing': 'Night (Weekly)',
                'total_tablets': tablets['dpearl'],
                'is_critical': False
            },
            {
                'name': 'T. Cetirizine 10mg',
                'tablets_per_day': 1,
                'timing': 'Night',
                'total_tablets': tablets['cetirizine'],
                'is_critical': False
            },
            {
                'name': 'Cap. Omeprazole 20mg',
                'tablets_per_day': 1,
                'timing': 'Morning (Before food)',
                'total_tablets': tablets['omeprazole'],
                'is_critical': False
            }
        ]

        # ─────────────────────────────────────────
        # STEP 4: Send daily alert email
        # ─────────────────────────────────────────
        send_medicine_alert(patient_name, medicines, caregiver_email)
        time.sleep(2)

        # ─────────────────────────────────────────
        # STEP 5: Generate PDF poster
        # ─────────────────────────────────────────
        create_medicine_poster(
            patient_name,
            medicines,
            filename="static/elderease_reminder.pdf"
        )

        # ─────────────────────────────────────────
        # STEP 6: Check stock & send reorder alert
        # ─────────────────────────────────────────
        reorder_data = send_reorder_alert(
            patient_name=patient_name,
            medicines=medicines,
            caregiver_email=caregiver_email,
            location=location
        )
        time.sleep(2)

        # ─────────────────────────────────────────
        # STEP 7: Weekly report (Mondays only)
        # ─────────────────────────────────────────
        weekly_sent = False
        if date.today().weekday() == 0:
            send_weekly_report(patient_name, medicines, caregiver_email)
            weekly_sent = True

        # ─────────────────────────────────────────
        # STEP 8: Build stock info for frontend
        # ─────────────────────────────────────────
        today = date.today()
        stock_info = []
        for med in medicines:
            days = med['total_tablets'] // med['tablets_per_day']
            finish = today + timedelta(days=days)
            reorder = today + timedelta(days=max(days - 2, 0))
            status = "urgent" if days <= 2 else "warning" if days <= 5 else "good"
            stock_info.append({
                'name': med['name'],
                'tablets': med['total_tablets'],
                'days': days,
                'finish': finish.strftime('%d %B %Y'),
                'reorder': reorder.strftime('%d %B %Y'),
                'status': status
            })

        # ─────────────────────────────────────────
        # STEP 9: Build reorder info for frontend
        # ─────────────────────────────────────────
        reorder_info = None
        if reorder_data and reorder_data.get('low_medicines'):
            reorder_info = {
                'low_medicines': reorder_data['low_medicines'],
                'urgent_medicines': reorder_data['urgent_medicines'],
                'whatsapp_link': reorder_data['whatsapp_link'],
                'pharmacy_map': reorder_data['pharmacy_map'],
                'whatsapp_text': reorder_data['whatsapp_text']
            }

        # Build response message
        messages = [f'✅ Daily alert sent to {caregiver_email}']
        if reorder_info:
            messages.append(f'🚨 Reorder alert sent for {len(reorder_info["low_medicines"])} medicine(s)')
        if weekly_sent:
            messages.append('📋 Weekly report sent!')

        return jsonify({
            'success': True,
            'prescription': prescription_result,
            'stock': stock_info,
            'reorder': reorder_info,
            'weekly_sent': weekly_sent,
            'message': ' | '.join(messages)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)