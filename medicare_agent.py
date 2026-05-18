import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from datetime import date, timedelta

load_dotenv()

# ============================================
# SETTING UP THE AI BRAIN (Gemini)
# ============================================
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# ============================================
# DEFINING OUR AGENTS (The Team Members)
# ============================================

prescription_agent = Agent(
    role="Medical Prescription Reader",
    goal="Read and understand doctor prescriptions and extract medicine details clearly",
    backstory="""You are an experienced medical assistant who has worked 
    with doctors for 20 years. You are expert at reading doctor's handwriting 
    and understanding medical abbreviations. You always provide clear, 
    structured medicine routines for patients.""",
    llm=llm,
    verbose=True
)

stock_tracker_agent = Agent(
    role="Medicine Stock Manager",
    goal="Track medicine stock levels and identify when reorders are needed",
    backstory="""You are a careful pharmacy stock manager who ensures 
    elderly patients never run out of their critical medicines. 
    You calculate stock levels precisely and always alert in advance 
    before medicines finish.""",
    llm=llm,
    verbose=True
)

care_coordinator_agent = Agent(
    role="Patient Care Coordinator",
    goal="Coordinate medicine reminders and send clear reports to caregivers and family",
    backstory="""You are a compassionate care coordinator who looks after 
    elderly patients. You communicate clearly with both patients and their 
    families, making sure everyone is informed about the patient's 
    medicine routine and health status.""",
    llm=llm,
    verbose=True
)

# ============================================
# DEFINING TASKS (What each agent does)
# ============================================

prescription_task = Task(
    description="""
    Analyze this prescription data and create a structured medicine routine:
    
    Patient: Jincy Varghese
    Medicines from prescription:
    1. Cap. D-Pearl 60k - 1 tablet - Night - Weekly - 8 weeks
    2. T. Cetirizine 10mg - 1 tablet - Night - Daily - 5 days  
    3. Cap. Omeprazole 20mg - 1 tablet - Morning before food - Daily - 5 days
    
    Create a clear, structured daily medicine schedule.
    """,
    expected_output="A structured medicine schedule with medicine names, dosage, timing and duration",
    agent=prescription_agent
)

stock_task = Task(
    description="""
    Based on the medicine schedule, analyze the stock levels:
    
    Current stock:
    - Cap. D-Pearl 60k: 8 tablets remaining
    - T. Cetirizine 10mg: 5 tablets remaining
    - Cap. Omeprazole 20mg: 5 tablets remaining
    
    Today's date: {today}
    
    Calculate:
    1. How many days each medicine will last
    2. Exact date when each medicine finishes
    3. Reorder date for each medicine (2 days before finish)
    4. Any urgent alerts needed
    """.format(today=date.today()),
    expected_output="Stock analysis report with finish dates, reorder dates and alerts",
    agent=stock_tracker_agent
)

care_task = Task(
    description="""
    Based on the medicine schedule and stock analysis, create a 
    comprehensive daily care report for the patient and caregiver.
    
    Include:
    1. Today's medicine schedule (what to take, when to take)
    2. Stock status summary
    3. Any urgent reorder alerts
    4. A warm, encouraging message for the elderly patient
    5. A summary for the family/caregiver
    
    Make it clear, simple and easy to understand for elderly people.
    """,
    expected_output="A complete daily care report with medicine schedule, stock alerts and caregiver summary",
    agent=care_coordinator_agent
)

# ============================================
# CREATING THE CREW (Assembling the team)
# ============================================

medicare_crew = Crew(
    agents=[prescription_agent, stock_tracker_agent, care_coordinator_agent],
    tasks=[prescription_task, stock_task, care_task],
    verbose=True
)

# ============================================
# RUNNING THE CREW (Let the team work!)
# ============================================

print("🏥 MediCare AI Agent Starting...")
print("=" * 50)

result = medicare_crew.kickoff()

print("\n" + "=" * 50)
print("✅ MEDICARE AI AGENT COMPLETE!")
print("=" * 50)
print(result)