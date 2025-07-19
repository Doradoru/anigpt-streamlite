import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# --------------------- CONFIGURATION ---------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
client = gspread.authorize(creds)

sheet_name = "AniGPT_DB"
try:
    sheet = client.open(sheet_name)
except:
    st.error(f"❌ Failed to open sheet: {sheet_name}")
    st.stop()

# --------------------- SHEET STRUCTURE ---------------------
required_tabs = {
    "Memory": ["Date", "User", "Memory"],
    "Mood logs": ["Date", "User", "Mood", "Trigger"],
    "Daily journal": ["Date", "User", "Summary", "Keywords"],
    "Learning": ["Date", "User", "WhatWasLearned", "Context"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "User", "Transcript"],
    "Anibook outline": ["Chapter", "Description", "User"],
    "Improvement notes": ["Date", "User", "Note"],
    "Quotes": ["Date", "User", "Quote"],
    "User facts": ["Fact", "User"],
    "Task done": ["Date", "User", "Task"],
    "Auto backup logs": ["Date", "User", "BackupStatus"]
}

# Ensure tabs and headers
for tab, headers in required_tabs.items():
    try:
        worksheet = sheet.worksheet(tab)
    except:
        worksheet = sheet.add_worksheet(title=tab, rows="100", cols="20")
    current_headers = worksheet.row_values(1)
    for i, h in enumerate(headers):
        if h not in current_headers:
            worksheet.update_cell(1, len(current_headers) + 1, h)
            current_headers.append(h)

# --------------------- UI ---------------------
st.title("🧠 AniGPT v2 – Your Personal Learning Assistant")

user = st.selectbox("👤 Select User", ["Ani", "Anne"])
user_input = st.text_area("💬 Enter your input below:")
submit = st.button("💾 Save to Google Sheet")

# --------------------- DETECTION LOGIC ---------------------
def detect_tab(text):
    text = text.lower()
    if any(word in text for word in ["udaas", "khushi", "sad", "happy", "mood"]):
        return "Mood logs"
    elif any(word in text for word in ["subah", "shaam", "utha", "soya", "routine", "kaam", "coding"]):
        return "Daily journal"
    elif any(word in text for word in ["learn", "seekha", "sikha", "understood", "pada", "padha"]):
        return "Learning"
    elif any(word in text for word in ["call", "remind", "yaad", "meeting", "alarm", "karna"]):
        return "Reminders"
    elif any(word in text for word in ["goal", "target", "dream", "sapna", "vision"]):
        return "Life goals"
    elif any(word in text for word in ["recorded", "audio", "voice", "mic"]):
        return "Voice logs"
    elif any(word in text for word in ["chapter", "book", "anibook", "outline"]):
        return "Anibook outline"
    elif any(word in text for word in ["improve", "sudhar", "mistake", "fix", "habit"]):
        return "Improvement notes"
    elif any(word in text for word in ["quote", "thought", "anmol", "line"]):
        return "Quotes"
    elif any(word in text for word in ["fact", "likes", "dislikes", "ani", "anne pasand"]):
        return "User facts"
    elif any(word in text for word in ["done", "complete", "finished", "kaam ho gaya"]):
        return "Task done"
    elif any(word in text for word in ["backup", "save", "copy"]):
        return "Auto backup logs"
    else:
        return "Memory"

# --------------------- SAVE DATA ---------------------
if submit and user_input:
    tab = detect_tab(user_input)
    ws = sheet.worksheet(tab)
    headers = ws.row_values(1)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Map columns to data
    data_dict = {
        "Date": date_str,
        "User": user,
        "Memory": user_input,
        "Mood": user_input,
        "Trigger": "",
        "Summary": user_input,
        "Keywords": "",
        "WhatWasLearned": user_input,
        "Context": "",
        "Task": user_input,
        "Time": "",
        "Status": "Pending",
        "Goal": user_input,
        "Category": "",
        "Target Date": "",
        "Progress": "",
        "Transcript": user_input,
        "Chapter": "",
        "Description": user_input,
        "Note": user_input,
        "Quote": user_input,
        "Fact": user_input,
        "Task": user_input,
        "BackupStatus": "Saved"
    }

    row = [data_dict.get(h, "") for h in headers]
    ws.append_row(row)
    st.success(f"✅ Saved to: {tab}")

