# Make.com Scenario Setup Guide

This guide walks you through importing and configuring the **AI-Powered Email Automation System** scenario on Make.com.

---

## Prerequisites

1. **Make.com Account**: Free or paid tier at [make.com](https://www.make.com/).
2. **Google Cloud / Workspace Account**: Access to Google Sheets and Gmail.
3. **Google AI Studio API Key**: Free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
4. **Google Sheet**: Create a new Google Sheet and import [`templates/leads_template.csv`](../templates/leads_template.csv).

---

## Step 1: Import Blueprint into Make.com

1. Log into your **Make.com** dashboard.
2. Click **Scenarios** in the left sidebar, then click **Create a new scenario** (top-right).
3. In the scenario canvas, click the **three dots (`...`)** menu at the bottom toolbar.
4. Select **Import Blueprint**.
5. Upload the file [`make-scenario-blueprint.json`](../make-scenario-blueprint.json).
6. Click **Save**. All 5 modules will be mapped onto the canvas.

---

## Step 2: Configure Module Connections

### Module 1: Google Sheets (Search Rows)
1. Click on **Module 1 (Fetch Pending Leads)**.
2. Under **Connection**, click **Add** and authenticate your Google account.
3. In **Search Method**, choose **Search Rows**.
4. In **Spreadsheet**, select your Google Sheet (e.g. `Leads Database`).
5. In **Sheet Name**, select the sheet tab (e.g. `Sheet1`).
6. In **Filter**, confirm:
   - Field: `Draft_Status`
   - Operator: `Equal to`
   - Value: `Pending`
7. Click **OK**.

### Module 2: HTTP (Gemini API Request)
1. Click on **Module 2 (Generate Draft with Gemini API)**.
2. In the **URL** field, replace `{{gemini_api_key}}` with your actual Google AI Studio API key:
   ```
   https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_ACTUAL_API_KEY
   ```
3. Ensure:
   - **Method**: `POST`
   - **Headers**: `Content-Type: application/json`
   - **Parse response**: `Yes`
4. Click **OK**.

### Module 3: JSON (Parse JSON)
1. Click on **Module 3 (Parse LLM JSON Response)**.
2. Verify the JSON input string maps to:
   ```
   {{2.data.candidates[1].content.parts[1].text}}
   ```
3. Click **OK**.

### Module 4: Gmail (Create a Draft)
1. Click on **Module 4 (Create Draft in Gmail)**.
2. Under **Connection**, connect your Gmail/Google Workspace account.
3. Verify mappings:
   - **To**: `{{1.Recipient_Email}}`
   - **Subject**: `{{3.subject}}`
   - **Content**: `{{3.body_html}}`
   - **Content type**: `HTML`
4. *Note*: Creating a draft ensures human-in-the-loop safety before any message is sent.
5. Click **OK**.

### Module 5: Google Sheets (Update a Row)
1. Click on **Module 5 (Update Row Status)**.
2. Select your Google Connection and Spreadsheet.
3. In **Row Number**, map `{{1.__ROW_NUMBER__}}`.
4. Under updated values:
   - `Draft_Status`: `Draft Created`
   - `Generated_Subject`: `{{3.subject}}`
   - `Generated_Body`: `{{3.body_plain}}`
   - `Draft_ID`: `{{4.id}}`
   - `Last_Updated`: `{{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}`
5. Click **OK**.

---

## Step 3: Test and Activate

1. Add a sample row in your Google Sheet with `Draft_Status = Pending`.
2. Click **Run once** (play button) at the bottom left of the Make designer.
3. Watch each bubble turn green.
4. Check your **Gmail Drafts folder**: you will see the AI-generated draft addressed to your test lead!
5. Check your **Google Sheet**: notice `Draft_Status` updated to `Draft Created` alongside the timestamp and generated subject.
6. Toggle the **Scheduling switch** at the bottom left to **ON** (e.g. Run every 15 minutes or every hour).
