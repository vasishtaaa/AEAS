# AI-Powered Email Automation System (AEAS)

![Make.com](https://img.shields.io/badge/Platform-Make.com-6D00F6?style=flat-square&logo=make)
![Gemini API](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-4285F4?style=flat-square&logo=google)
![Google Sheets](https://img.shields.io/badge/Database-Google%20Sheets-34A853?style=flat-square&logo=googlesheets)
![Gmail API](https://img.shields.io/badge/Delivery-Gmail%20Drafts-EA4335?style=flat-square&logo=gmail)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

An automated end-to-end B2B email generation pipeline built on **Make.com**, connecting **Google Sheets**, **Google Gemini 1.5 Flash API**, and **Gmail**. The system monitors new and qualified prospect leads, synthesizes hyper-personalized outreach drafts tailored to specific pain points, and records audit states in Google Sheets with human-in-the-loop review.

---

## 🌟 Key Features

- **Automated Lead Intake**: Polling engine watches Google Sheets for rows marked `Draft_Status = Pending`.
- **Context-Aware Prompt Engineering**: Supplies lead metadata (role, industry, pain points, value proposition) into Gemini 1.5 Flash.
- **Structured JSON Synthesis**: Utilizes Gemini's native `responseMimeType: "application/json"` to generate validated subject lines, HTML bodies, and plain-text fallbacks.
- **Human-In-The-Loop Drafts**: Creates drafts directly in Gmail instead of auto-sending, allowing one-click review and personalization touches before dispatch.
- **State Synchronization & Audit Trail**: Updates each Google Sheet row with timestamp, draft ID, and status (`Draft Created`), preventing duplicate generation.

---

## 🏗️ Architecture & Data Flow

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────────┐
│  Google Sheets  │ ----> │    Make.com     │ ----> │  Gemini 1.5 Flash   │
│ (Pending Leads) │       │ (Orchestrator)  │       │ (JSON Prompt Model) │
└─────────────────┘       └────────┬────────┘       └──────────┬──────────┘
                                   │                           │
                                   │ <─────────────────────────┘
                                   ▼
                        ┌─────────────────────┐
                        │     Gmail API       │
                        │ (Create Draft Inbox)│
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  Google Sheets Row  │
                        │ (Status Update: OK) │
                        └─────────────────────┘
```

---

## 📂 Repository Structure

```
AEAS/
├── make-scenario-blueprint.json   # Ready-to-import Make.com scenario blueprint
├── templates/
│   └── leads_template.csv         # Starter Google Sheet schema with test rows
├── prompts/
│   ├── system_prompt.txt          # Copywriting persona and structure rules
│   └── gemini_prompt_template.json # API payload definition with schema constraints
├── docs/
│   └── MAKE_SETUP_GUIDE.md        # Step-by-step import & connection walkthrough
├── scripts/
│   └── test_gemini_prompt.py      # Local Python validation script for Gemini API
├── requirements.txt               # Dependencies for test script
├── .env.example                   # Environment configuration template
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Prepare Google Sheets
1. Create a new Google Spreadsheet (e.g. `B2B Outreach Database`).
2. Import the sample header schema from [`templates/leads_template.csv`](templates/leads_template.csv):
   - `Lead_ID`
   - `Recipient_Name`
   - `Recipient_Email`
   - `Company_Name`
   - `Industry`
   - `Company_Role`
   - `Context_Pain_Points`
   - `Offer_Angle`
   - `Draft_Status` (Set to `Pending` to trigger)
   - `Generated_Subject`
   - `Generated_Body`
   - `Draft_ID`
   - `Last_Updated`

### 2. Import Scenario into Make.com
1. In Make.com, create a **New Scenario**.
2. Click `...` in the bottom bar and select **Import Blueprint**.
3. Choose [`make-scenario-blueprint.json`](make-scenario-blueprint.json).
4. Follow the detailed steps in [docs/MAKE_SETUP_GUIDE.md](docs/MAKE_SETUP_GUIDE.md) to connect:
   - Your Google Sheets account
   - Your Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Your Gmail account

### 3. (Optional) Test Locally with Python
To test your Gemini API key and prompt output without launching Make.com:
```bash
# Clone the repository
git clone <your-repo-url>
cd AEAS

# Install requirements
pip install -r requirements.txt

# Configure API Key
cp .env.example .env
# edit .env and set GEMINI_API_KEY=your_key

# Run test script
python scripts/test_gemini_prompt.py
```

---

## 🛡️ Safety & Reliability

- **Human-in-the-Loop**: Drafts are placed in Gmail Drafts rather than dispatches to prevent unintended emails.
- **Strict JSON Enforcement**: `responseMimeType: "application/json"` guarantees reliable module parsing in Make.com.
- **Idempotency**: Rows marked `Draft Created` are skipped on subsequent polling runs.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
