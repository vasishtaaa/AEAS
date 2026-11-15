import os
import json
import sys
from dotenv import load_dotenv

# Try importing official SDK, fallback to urllib if not installed
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SAMPLE_LEAD = {
    "Recipient_Name": "Sarah Jenkins",
    "Recipient_Email": "sarah.jenkins@acmefintech.io",
    "Company_Name": "Acme FinTech",
    "Company_Role": "VP of Growth",
    "Industry": "Financial Services",
    "Context_Pain_Points": "High customer acquisition costs, struggling with lead follow-up speed",
    "Offer_Angle": "Automated CRM lead nurturing with 2-minute response time"
}

def test_prompt_direct():
    if not GEMINI_API_KEY:
        print("[!] GEMINI_API_KEY environment variable is missing.")
        print("    Copy .env.example to .env and insert your API key from https://aistudio.google.com/app/apikey")
        sys.exit(1)

    try:
        import requests
    except ImportError:
        import urllib.request
        import urllib.error
        requests = None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "system_instruction": {
            "parts": [
                {
                    "text": (
                        "You are an elite B2B email copywriter. Write highly personalized, concise "
                        "(<125 words) outreach emails based strictly on the prospect metadata. "
                        "Respond strictly in valid JSON format with keys: 'subject', 'body_plain', 'body_html', 'reasoning'."
                    )
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            f"Lead Details:\n"
                            f"- Name: {SAMPLE_LEAD['Recipient_Name']}\n"
                            f"- Email: {SAMPLE_LEAD['Recipient_Email']}\n"
                            f"- Company: {SAMPLE_LEAD['Company_Name']}\n"
                            f"- Role: {SAMPLE_LEAD['Company_Role']}\n"
                            f"- Industry: {SAMPLE_LEAD['Industry']}\n"
                            f"- Pain Points: {SAMPLE_LEAD['Context_Pain_Points']}\n"
                            f"- Offer: {SAMPLE_LEAD['Offer_Angle']}\n\n"
                            "Generate the tailored cold email in JSON format."
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.95,
            "maxOutputTokens": 1024,
            "responseMimeType": "application/json"
        }
    }

    print("[*] Dispatching test request to Gemini 1.5 Flash...")

    if requests:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if res.status_code != 200:
            print(f"[!] API Error ({res.status_code}): {res.text}")
            return
        data = res.json()
    else:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"[!] HTTP Error ({e.code}): {e.read().decode('utf-8')}")
            return

    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    result = json.loads(raw_text)

    print("\n[+] Successfully generated email response from Gemini:")
    print("-" * 60)
    print(f"Subject: {result.get('subject')}")
    print(f"\nBody (Plain):\n{result.get('body_plain')}")
    print(f"\nReasoning:\n{result.get('reasoning')}")
    print("-" * 60)

if __name__ == "__main__":
    test_prompt_direct()
