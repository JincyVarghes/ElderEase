import os
import time
from datetime import date, timedelta
from dotenv import load_dotenv

# Import all our modules
from prescription_reader import read_prescription_image
from medicine_tracker import track_medicines
from alert_system import send_medicine_alert
from reminder_poster import create_medicine_poster
from weekly_report import send_weekly_report

load_dotenv()

def run_elderease_agent():
    print("\n" + "="*60)
    print("💙  ELDEREASE AI AGENT STARTING...")
    print("    Smart Medicine Care for Elderly People")
    print("="*60 + "\n")

    # ─────────────────────────────────────────
    # PATIENT DETAILS
    # ─────────────────────────────────────────
    patient_name = "Jincy Varghese"
    caregiver_email = "jincy.builds@gmail.com"
    prescription_image = "prescription.jpg"

    medicines = [
        {
            'name': 'Cap. D-Pearl 60k',
            'tablets_per_day': 1,
            'timing': 'Night (Weekly)',
            'total_tablets': 8,
            'is_critical': False
        },
        {
            'name': 'T. Cetirizine 10mg',
            'tablets_per_day': 1,
            'timing': 'Night',
            'total_tablets': 5,
            'is_critical': False
        },
        {
            'name': 'Cap. Omeprazole 20mg',
            'tablets_per_day': 1,
            'timing': 'Morning (Before food)',
            'total_tablets': 5,
            'is_critical': False
        }
    ]

    # ─────────────────────────────────────────
    # STEP 1: READ PRESCRIPTION IMAGE
    # ─────────────────────────────────────────
    print("📸 STEP 1: Reading Prescription Image...")
    print("-"*40)
    prescription_result = read_prescription_image(prescription_image)
    print(prescription_result)
    print("✅ Prescription read successfully!\n")
    time.sleep(2)

    # ─────────────────────────────────────────
    # STEP 2: TRACK MEDICINE STOCK
    # ─────────────────────────────────────────
    print("📊 STEP 2: Tracking Medicine Stock...")
    print("-"*40)
    track_medicines(medicines)
    print("✅ Stock tracking complete!\n")
    time.sleep(2)

    # ─────────────────────────────────────────
    # STEP 3: SEND DAILY ALERT EMAIL
    # ─────────────────────────────────────────
    print("📧 STEP 3: Sending Daily Alert Email...")
    print("-"*40)
    send_medicine_alert(patient_name, medicines, caregiver_email)
    print("✅ Daily alert sent!\n")
    time.sleep(2)

    # ─────────────────────────────────────────
    # STEP 4: GENERATE PDF POSTER
    # ─────────────────────────────────────────
    print("🖨️  STEP 4: Generating Medicine Reminder Poster...")
    print("-"*40)
    create_medicine_poster(patient_name, medicines, 
                          filename="elderease_reminder.pdf")
    print("✅ Poster generated!\n")
    time.sleep(2)

    # ─────────────────────────────────────────
    # STEP 5: SEND WEEKLY REPORT (on Mondays)
    # ─────────────────────────────────────────
    today = date.today()
    if today.weekday() == 0:  # 0 = Monday
        print("📋 STEP 5: Sending Weekly Report (Monday)...")
        print("-"*40)
        send_weekly_report(patient_name, medicines, caregiver_email)
        print("✅ Weekly report sent!\n")
    else:
        print(f"📋 STEP 5: Weekly report skipped (sends every Monday)")
        print(f"   Next report on: {(today + timedelta(days=(7 - today.weekday()))).strftime('%d %B %Y')}\n")

    # ─────────────────────────────────────────
    # STEP 6: RUN CREWAI MULTI-AGENT SYSTEM
    # ─────────────────────────────────────────
    print("🤖 STEP 6: Running ElderEase AI Agent Team...")
    print("-"*40)

    from crewai import Agent, Task, Crew, LLM
    from google import genai

    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prescription_agent = Agent(
        role="Medical Prescription Reader",
        goal="Read and understand doctor prescriptions and extract medicine details clearly",
        backstory="""You are an experienced medical assistant who has worked 
        with doctors for 20 years. You are expert at reading doctor's handwriting 
        and understanding medical abbreviations. You always provide clear, 
        structured medicine routines for elderly patients.""",
        llm=llm,
        verbose=False
    )

    stock_tracker_agent = Agent(
        role="Medicine Stock Manager",
        goal="Track medicine stock levels and identify when reorders are needed",
        backstory="""You are a careful pharmacy stock manager who ensures 
        elderly patients never run out of their critical medicines. 
        You calculate stock levels precisely and always alert in advance 
        before medicines finish.""",
        llm=llm,
        verbose=False
    )

    care_coordinator_agent = Agent(
        role="Patient Care Coordinator",
        goal="Coordinate medicine reminders and send clear reports to caregivers and family",
        backstory="""You are a compassionate care coordinator who looks after 
        elderly patients. You communicate clearly with both patients and their 
        families, making sure everyone is informed about the patient's 
        medicine routine and health status.""",
        llm=llm,
        verbose=False
    )

    prescription_task = Task(
        description=f"""
        Analyze this prescription data and create a structured medicine routine:
        Patient: {patient_name}
        Medicines:
        1. Cap. D-Pearl 60k - 1 tablet - Night - Weekly - 8 weeks
        2. T. Cetirizine 10mg - 1 tablet - Night - Daily - 5 days
        3. Cap. Omeprazole 20mg - 1 tablet - Morning before food - Daily - 5 days
        Create a clear structured daily medicine schedule.
        """,
        expected_output="A structured medicine schedule with medicine names, dosage, timing and duration",
        agent=prescription_agent
    )

    stock_task = Task(
        description=f"""
        Based on the medicine schedule, analyze stock levels:
        Current stock:
        - Cap. D-Pearl 60k: 8 tablets remaining
        - T. Cetirizine 10mg: 5 tablets remaining
        - Cap. Omeprazole 20mg: 5 tablets remaining
        Today's date: {date.today()}
        Calculate finish dates, reorder dates and urgent alerts.
        """,
        expected_output="Stock analysis report with finish dates, reorder dates and alerts",
        agent=stock_tracker_agent
    )

    care_task = Task(
        description=f"""
        Create a comprehensive daily care report for {patient_name} and caregiver.
        Include today's medicine schedule, stock status, urgent reorder alerts,
        a warm encouraging message for the elderly patient,
        and a summary for the family/caregiver.
        Make it clear and simple for elderly people.
        """,
        expected_output="Complete daily care report with medicine schedule, stock alerts and caregiver summary",
        agent=care_coordinator_agent
    )

    elderease_crew = Crew(
        agents=[prescription_agent, stock_tracker_agent, care_coordinator_agent],
        tasks=[prescription_task, stock_task, care_task],
        verbose=False
    )

    result = elderease_crew.kickoff()
    print(result)
    print("✅ ElderEase AI Agent Team completed!\n")

    # ─────────────────────────────────────────
    # DONE!
    # ─────────────────────────────────────────
    print("="*60)
    print("✅  ELDEREASE AI AGENT COMPLETED SUCCESSFULLY!")
    print(f"    Patient  : {patient_name}")
    print(f"    Date     : {date.today().strftime('%d %B %Y')}")
    print(f"    Email    : {caregiver_email}")
    print(f"    Poster   : elderease_reminder.pdf")
    print("💙  Keeping elderly people healthy and happy!")
    print("="*60 + "\n")

# RUN ELDEREASE
if __name__ == "__main__":
    run_elderease_agent()