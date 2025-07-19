import streamlit as st
import gspread
from datetime import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials

# --- Load credentials from secrets ---
json_key = json.loads(st.secrets["GOOGLE_SHEET_JSON"])

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
client = gspread.authorize(credentials)

# --- Open your sheet ---
spreadsheet = client.open("AniGPT_DB")  # Your Google Sheet name

# --- All required tabs ---
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders",
    "Life goals", "Voice logs", "Anibook outline", "Improvement notes",
    "Quotes", "User facts", "Task done", "Auto backup logs"
]

# --- Ensure all tabs exist ---
existing_tabs = [ws.title for ws in spreadsheet.worksheets()]
for tab in required_tabs:
    if tab not in existing_tabs:
        spreadsheet.add_worksheet(title=tab, rows="100", cols="20")

# --- Function: Ensure required headers exist ---
def ensure_headers(ws, headers):
    current = ws.row_values(1)
    for i, h in enumerate(headers):
        if h not in current:
            ws.update_cell(1, len(current) + 1, h)
            current.append(h)

# --- Function: Smart tab detection based on input ---
def detect_tab(text):
    text = text.lower()
    if any(word in text for word in ["happy", "sad", "angry", "tired", "excited", "mood"]):
        return "Mood logs"
    elif any(word in text for word in ["learned", "sikh", "understood", "study"]):
        return "Learning"
    elif any(word in text for word in ["goal", "target", "dream", "future"]):
        return "Life goals"
    elif any(word in text for word in ["note", "improve", "fix", "bad habit"]):
        return "Improvement notes"
    elif any(word in text for word in ["quote", "motivation", "line"]):
        return "Quotes"
    elif any(word in text for word in ["journal", "summary", "reflection", "day", "din"]):
        return "Daily journal"
    elif any(word in text for word in ["task", "kaam", "done", "complete"]):
        return "Task done"
    elif any(word in text for word in ["voice", "audio", "mic", "record"]):
        return "Voice logs"
    elif any(word in text for word in ["remind", "yaad", "kal", "aaj"]):
        return "Reminders"
    else:
        return "Memory"

# --- Streamlit UI ---
st.title("🧠 AniGPT v2 – Smart Input Saver")

# Dropdown to select user
user = st.selectbox("👤 Select User", ["Ani", "Anne"])

# Text input
user_input = st.text_area("💬 Enter your thought, journal, task, or anything...")

if st.button("💾 Save to Google Sheet"):
    if user_input.strip() == "":
        st.warning("Please enter something before submitting.")
    else:
        tab = detect_tab(user_input)
        ws = spreadsheet.worksheet(tab)

        # Prepare row
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headers = ws.row_values(1)

        # Ensure required columns exist
        required_columns = ["User", "Date", "Input"]
        ensure_headers(ws, required_columns)

        row = []
        for col in required_columns:
            if col == "User":
                row.append(user)
            elif col == "Date":
                row.append(now)
            elif col == "Input":
                row.append(user_input)

        ws.append_row(row)
        st.success(f"✅ Saved to **{tab}** tab.")
