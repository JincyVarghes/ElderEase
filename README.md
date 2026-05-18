# 💙 ElderEase — Smart Medicine Care AI Agent

> AI-powered medication management system for elderly people, built with Python, CrewAI and Gemini AI.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-MultiAgent-green)
![Flask](https://img.shields.io/badge/Flask-WebApp-lightgrey)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 About ElderEase

ElderEase was born from a failed mobile app idea that I reimagined as a fully working AI Agent system. It solves a real problem — elderly patients (especially those whose families live abroad) often miss medicines, run out of stock, or have no one to monitor their health routine.

ElderEase uses multiple AI agents working together to automate the entire medicine management process — from reading a doctor's handwritten prescription to automatically alerting the family and reordering medicines before they run out.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📸 Prescription Reader | Reads handwritten doctor prescriptions using Gemini Vision AI |
| 💊 Stock Tracker | Tracks tablet count and calculates exact finish dates |
| 📧 Daily Email Alerts | Sends medicine reminders to patient and caregiver |
| 🖨️ PDF Poster | Generates large font medicine reminder poster for elderly |
| 📋 Weekly Report | Sends detailed weekly health report to family abroad |
| 🚨 Reorder Alerts | Automatically detects low stock and sends reorder alerts |
| 💬 WhatsApp Order | Generates ready-to-send WhatsApp message to pharmacy |
| 📍 Nearby Pharmacy | Finds nearby medical shops on Google Maps |
| 🤖 Multi-Agent AI | Powered by CrewAI with 3 specialized AI agents |
| 🌐 Web Interface | Beautiful web app — upload prescription and everything runs automatically |

---

## 🤖 AI Agents

ElderEase uses **3 specialized AI agents** working as a team:

| Agent | Role |
|-------|------|
| 🧠 Medical Prescription Reader Agent | Reads and interprets doctor's handwriting |
| 📊 Medicine Stock Manager Agent | Tracks stock levels and calculates reorder dates |
| 💙 Patient Care Coordinator Agent | Creates daily care reports for patient and family |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.13 | Core programming language |
| CrewAI | Multi-agent AI framework |
| Google Gemini 2.5 Flash | AI model for prescription reading and reports |
| Flask | Web application framework |
| ReportLab | PDF generation |
| SMTP / Gmail | Email automation |
| HTML / CSS / JavaScript | Frontend web interface |
| Geopy | Location services |

---

## 📁 Project Structure

    ElderEase/
    │
    ├── app.py                  Flask web application (main entry point)
    ├── main.py                 CLI entry point for running agent directly
    ├── medicare_agent.py       CrewAI multi-agent system
    ├── prescription_reader.py  Gemini AI prescription image reader
    ├── medicine_tracker.py     Medicine stock tracking logic
    ├── alert_system.py         Daily email alert system
    ├── reminder_poster.py      PDF poster generator
    ├── weekly_report.py        Weekly family report system
    ├── reorder_system.py       Auto reorder + WhatsApp + Maps feature
    │
    ├── templates/
    │   └── index.html          Web interface frontend
    │
    ├── static/                 Generated PDF posters stored here
    ├── uploads/                Uploaded prescription images stored here
    │
    ├── .env                    API keys (not uploaded to GitHub)
    ├── .gitignore              Git ignore file
    ├── requirements.txt        Python dependencies
    └── README.md               Project documentation

---

## 🚀 How It Works

    1. User uploads prescription photo via web interface
    2. Gemini Vision AI reads handwritten prescription
    3. Medicine routine is extracted and structured
    4. Stock levels are tracked and analyzed
    5. Daily reminder email sent to caregiver
    6. Large font PDF reminder poster generated
    7. Low stock detected → Reorder alert email sent
    8. WhatsApp message + Google Maps pharmacy link shared
    9. Weekly report sent to family every Monday
    10. CrewAI multi-agent team generates complete care report

---

## ⚙️ Setup & Installation

### 1. Clone the repository

    git clone https://github.com/JincyVarghes/ElderEase.git
    cd ElderEase

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Create .env file

Create a file named `.env` in the root folder and add:

    GEMINI_API_KEY=your_gemini_api_key_here
    EMAIL_ADDRESS=your_gmail@gmail.com
    EMAIL_PASSWORD=your_16_digit_app_password

### 4. Get your API keys

**Gemini API Key (Free):**
- Go to [aistudio.google.com](https://aistudio.google.com)
- Click Get API Key → Create API Key
- Copy and paste into .env file

**Gmail App Password:**
- Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Create a new app password named ElderEase
- Copy the 16 digit password into .env file

### 5. Run the web app

    python app.py

### 6. Open in browser

    http://127.0.0.1:5000

---

## 📸 Usage

1. Open ElderEase in your browser at http://127.0.0.1:5000
2. Enter **patient name** and **caregiver email**
3. Enter **patient location** for nearby pharmacy search
4. Enter **current medicine stock** counts
5. Upload **prescription photo** taken from phone camera
6. Click **Run ElderEase AI Agent**
7. Everything happens automatically! ✅

**What happens automatically:**
- ✅ Prescription is read by AI
- ✅ Stock levels are calculated
- ✅ Daily reminder email is sent
- ✅ PDF poster is generated
- ✅ Reorder alert sent if stock is low
- ✅ WhatsApp pharmacy order message generated
- ✅ Nearby pharmacy shown on Google Maps
- ✅ Weekly report sent every Monday

---

## 📋 Requirements

    flask
    crewai
    google-genai
    python-dotenv
    reportlab
    geopy
    werkzeug

---

## 💡 Project Story

This project started as a mobile app idea called **Elderease** during my academic mini project. We failed to implement it as a mobile app due to technical limitations at the time.

I reimagined and rebuilt it as a complete **AI Agent system** using Python, CrewAI and Gemini AI.

**What I learned building this project:**
- Multi-agent AI systems with CrewAI
- Multimodal AI — reading images with Gemini Vision
- REST API integration
- Email automation with Python SMTP
- PDF generation with ReportLab
- Full-stack web development with Flask
- Git and GitHub version control

---

## 🔮 Future Improvements

- Mobile app with camera integration
- Real pharmacy API integration
- Push notifications on mobile
- Support for multiple patients
- Voice reminders for elderly
- Medicine interaction checker
- Cloud deployment on AWS or Google Cloud

---

## 👩‍💻 Built By

**Jincy Varghese**
- GitHub: [@JincyVarghes](https://github.com/JincyVarghes)
- Email: jincy.builds@gmail.com

---

## 🙏 Acknowledgements

- [CrewAI](https://crewai.com) — Multi-agent AI framework
- [Google Gemini](https://ai.google.dev) — AI model
- [Flask](https://flask.palletsprojects.com) — Web framework
- [ReportLab](https://reportlab.com) — PDF generation

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> 💙 *"Keeping elderly people healthy, happy and cared for — one prescription at a time."*