import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_medicine_alert(patient_name, medicines, caregiver_email):
    print("=== SENDING MEDICINE ALERT EMAIL ===\n")
    
    today = date.today().strftime("%d %B %Y")
    
    # Build email body
    medicine_list_html = ""
    for med in medicines:
        medicine_list_html += f"""
        <tr>
            <td style="padding:8px; border:1px solid #ddd;">{med['name']}</td>
            <td style="padding:8px; border:1px solid #ddd;">{med['tablets_per_day']} tablet(s)</td>
            <td style="padding:8px; border:1px solid #ddd;">{med['timing']}</td>
            <td style="padding:8px; border:1px solid #ddd;">{med['total_tablets']} left</td>
        </tr>
        """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 16px;">
        <h2 style="color: #2e86c1;">💊 Daily Medicine Reminder</h2>
        <p>Dear <b>{patient_name}</b>,</p>
        <p>Date: <b>{today}</b></p>
        <p>Here are your medicines for today:</p>
        
        <table style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #2e86c1; color: white;">
                <th style="padding:8px;">Medicine</th>
                <th style="padding:8px;">Dose</th>
                <th style="padding:8px;">Timing</th>
                <th style="padding:8px;">Stock Left</th>
            </tr>
            {medicine_list_html}
        </table>
        
        <br>
        <p style="color: #e74c3c;"><b>⚠️ Please do not skip your medicines!</b></p>
        <p>Stay healthy and happy! 😊</p>
        <br>
        <p style="color: #888; font-size: 12px;">Sent by MediCare AI Agent</p>
    </body>
    </html>
    """

    # Create email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"💊 Medicine Reminder for {patient_name} - {today}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = caregiver_email
    msg.attach(MIMEText(html_body, "html"))

    # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, caregiver_email, msg.as_string())
        print(f"✅ Email sent successfully to {caregiver_email}!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Test with your prescription data
medicines = [
    {
        'name': 'Cap. D-Pearl 60k',
        'tablets_per_day': 1,
        'timing': 'Night (Weekly)',
        'total_tablets': 8
    },
    {
        'name': 'T. Cetirizine 10mg',
        'tablets_per_day': 1,
        'timing': 'Night',
        'total_tablets': 5
    },
    {
        'name': 'Cap. Omeprazole 20mg',
        'tablets_per_day': 1,
        'timing': 'Morning (Before food)',
        'total_tablets': 5
    }
]

send_medicine_alert(
    patient_name="Jincy Varghese",
    medicines=medicines,
    caregiver_email="jincy.builds@gmail.com"
)