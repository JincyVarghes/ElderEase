import os
import smtplib
import webbrowser
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_whatsapp_message(patient_name, low_medicines):
    message = f"Hello, I would like to order medicines for {patient_name}:\n\n"
    for med in low_medicines:
        message += f"• {med['name']} — {med['quantity']} strips/units\n"
    message += "\nKindly confirm availability and price. Thank you."
    return message

def get_pharmacy_links(location="Chengamanad, Ernakulam, Kerala"):
    encoded = urllib.parse.quote(f"medical shops near {location}")
    google_maps = f"https://www.google.com/maps/search/{encoded}"
    return google_maps

def send_reorder_alert(patient_name, medicines, caregiver_email,
                      location="Chengamanad, Ernakulam, Kerala"):
    print("\n=== ELDEREASE REORDER SYSTEM ===\n")

    today = date.today()

    # Find medicines that need reordering
    low_medicines = []
    urgent_medicines = []

    for med in medicines:
        days_left = med['total_tablets'] // med['tablets_per_day']
        if days_left <= 2:
            urgent_medicines.append({
                'name': med['name'],
                'days_left': days_left,
                'quantity': 2,
                'timing': med['timing']
            })
            low_medicines.append({
                'name': med['name'],
                'days_left': days_left,
                'quantity': 2,
                'timing': med['timing']
            })
        elif days_left <= 5:
            low_medicines.append({
                'name': med['name'],
                'days_left': days_left,
                'quantity': 2,
                'timing': med['timing']
            })

    if not low_medicines:
        print("✅ All medicines have sufficient stock. No reorder needed!")
        return

    # Generate WhatsApp message
    whatsapp_text = generate_whatsapp_message(patient_name, low_medicines)
    whatsapp_encoded = urllib.parse.quote(whatsapp_text)
    whatsapp_link = f"https://wa.me/?text={whatsapp_encoded}"

    # Get pharmacy map link
    pharmacy_map = get_pharmacy_links(location)

    # Build email
    urgent_html = ""
    if urgent_medicines:
        urgent_html = """
        <div style="background:#fdedec; border-left:4px solid #e74c3c;
                    padding:1rem; border-radius:8px; margin-bottom:1rem;">
            <h3 style="color:#c0392b; margin:0 0 0.5rem;">
                🚨 URGENT — Stock Almost Finished!
            </h3>
        """
        for med in urgent_medicines:
            urgent_html += f"""
            <p style="margin:4px 0; color:#c0392b; font-weight:500;">
                ⚠️ {med['name']} — Only {med['days_left']} day(s) left!
            </p>
            """
        urgent_html += "</div>"

    medicines_html = ""
    for med in low_medicines:
        status_color = "#c0392b" if med['days_left'] <= 2 else "#e67e22"
        medicines_html += f"""
        <tr>
            <td style="padding:10px; border:1px solid #eee;">
                {med['name']}
            </td>
            <td style="padding:10px; border:1px solid #eee; color:{status_color};
                       font-weight:500;">
                {med['days_left']} day(s) left
            </td>
            <td style="padding:10px; border:1px solid #eee;">
                {med['timing']}
            </td>
            <td style="padding:10px; border:1px solid #eee;">
                2 strips
            </td>
        </tr>
        """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size:16px;
                 max-width:700px; margin:auto; padding:20px;">

        <div style="background:linear-gradient(135deg,#1a5276,#2e86c1);
                    padding:20px; border-radius:12px; text-align:center;
                    margin-bottom:1.5rem;">
            <h1 style="color:white; margin:0; font-size:1.6rem;">
                💙 ElderEase — Reorder Alert
            </h1>
            <p style="color:white; margin:5px 0; opacity:0.9;">
                Patient: {patient_name} | Date: {today.strftime('%d %B %Y')}
            </p>
        </div>

        {urgent_html}

        <h2 style="color:#1a5276;">💊 Medicines That Need Reordering</h2>
        <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
            <tr style="background:#2e86c1; color:white;">
                <th style="padding:10px;">Medicine</th>
                <th style="padding:10px;">Stock Status</th>
                <th style="padding:10px;">Timing</th>
                <th style="padding:10px;">Order Qty</th>
            </tr>
            {medicines_html}
        </table>

        <h2 style="color:#1a5276;">📍 Find Nearby Pharmacy</h2>
        <p style="color:#445566;">
            Click the button below to find medical shops near
            <b>{location}</b>:
        </p>
        <div style="text-align:center; margin:1rem 0;">
            <a href="{pharmacy_map}"
               style="background:#2e86c1; color:white; padding:12px 24px;
                      border-radius:8px; text-decoration:none; font-weight:500;
                      font-size:1rem;">
                📍 Find Nearby Pharmacy on Google Maps
            </a>
        </div>

        <h2 style="color:#1a5276;">💬 Ready-to-Send WhatsApp Message</h2>
        <p style="color:#445566;">
            Copy and send this message to your local pharmacy on WhatsApp,
            or click the button to open WhatsApp directly:
        </p>
        <div style="background:#f0f4f8; border-radius:8px; padding:1rem;
                    margin-bottom:1rem; font-size:0.95rem; color:#334455;
                    white-space:pre-wrap; line-height:1.7;">
{whatsapp_text}
        </div>
        <div style="text-align:center; margin:1rem 0;">
            <a href="{whatsapp_link}"
               style="background:#25d366; color:white; padding:12px 24px;
                      border-radius:8px; text-decoration:none; font-weight:500;
                      font-size:1rem;">
                💬 Open WhatsApp & Send Order
            </a>
        </div>

        <div style="background:#eaf4fd; border-radius:8px; padding:1rem;
                    margin-top:1.5rem;">
            <p style="color:#1a5276; font-weight:500; margin:0;">
                💡 Tip: Order medicines at least 2 days before they finish
                to avoid any gap in treatment!
            </p>
        </div>

        <div style="background:#2e86c1; padding:15px; border-radius:8px;
                    margin-top:1.5rem; text-align:center;">
            <p style="color:white; margin:0; font-size:0.9rem;">
                💙 ElderEase AI Agent — Keeping elderly people healthy and happy!
            </p>
        </div>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 ElderEase Reorder Alert — {patient_name} — {today.strftime('%d %B %Y')}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = caregiver_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, caregiver_email, msg.as_string())
        print(f"✅ Reorder alert email sent to {caregiver_email}!")
        print(f"📍 Pharmacy map: {pharmacy_map}")
        print(f"💬 WhatsApp message ready!")
    except Exception as e:
        print(f"❌ Error: {e}")

    return {
        'low_medicines': low_medicines,
        'urgent_medicines': urgent_medicines,
        'whatsapp_link': whatsapp_link,
        'pharmacy_map': pharmacy_map,
        'whatsapp_text': whatsapp_text
    }

# Test
medicines = [
    {
        'name': 'Cap. D-Pearl 60k',
        'tablets_per_day': 1,
        'timing': 'Night (Weekly)',
        'total_tablets': 8,
    },
    {
        'name': 'T. Cetirizine 10mg',
        'tablets_per_day': 1,
        'timing': 'Night',
        'total_tablets': 3,
    },
    {
        'name': 'Cap. Omeprazole 20mg',
        'tablets_per_day': 1,
        'timing': 'Morning (Before food)',
        'total_tablets': 2,
    }
]

send_reorder_alert(
    patient_name="Jincy Varghese",
    medicines=medicines,
    caregiver_email="jincy.builds@gmail.com",
    location="Chengamanad, Ernakulam, Kerala"
)