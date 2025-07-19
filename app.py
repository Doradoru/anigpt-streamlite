import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import datetime

st.set_page_config(page_title="AniGPT v2 – Auto Tab", layout="centered")

# 📌 Tabs and Headings Setup
tabs_with_headings = {
    "Memory": ["Date", "Memory", "User"],
    "Mood logs": ["Date", "Mood", "Trigger", "User"],
    "Daily journal": ["Date", "Summary", "Keywords", "User"],
    "Learning": ["Date", "WhatWasLearned", "Context", "User"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "Note", "User"],
    "Anibook outline": ["Section", "Summary", "Notes", "User"],
    "Improvement notes": ["Date", "Issue", "Solution", "User"],
    "Quotes": ["Quote", "Author", "Mood", "User"],
    "User facts": ["Fact", "Context", "Date", "User"],
    "Task done": ["Task", "Date", "Status", "User"],
    "Auto backup logs": ["DateTime", "DataType", "Status", "User"]
}

# 🔐 Google Sheets Auth
json_key = st.secrets["GOOGLE_SHEET_JSON"]

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

SHEET_NAME = "AniGPT_DB"
spreadsheet = client.open(SHEET_NAME)

# 🛠️ Create missing tabs and set headings
def ensure_tabs():
    for tab_name, headers in tabs_with_headings.items():
        try:
            ws = spreadsheet.worksheet(tab_name)
        except gspread.WorksheetNotFound:
            ws = spreadsheet.add_worksheet(title=tab_name, rows="100", cols=str(len(headers)))
        current_headers = ws.row_values(1)
        if current_headers != headers:
            ws.resize(rows=100, cols=len(headers))
            ws.delete_rows(1)
            ws.insert_row(headers, index=1)

ensure_tabs()

# 🎛️ UI
st.title("🧠 AniGPT v2 – Auto Smart Entry")
user = st.selectbox("👤 Select User", ["Ani", "Anne"])
text_input = st.text_area("📌 What's on your mind?", height=150)
submit = st.button("💾 Save")

# 🤖 Tab Detector Function
def detect_tab(text):
    text_lower = text.lower()
    if "learn" in text_lower or "seekha" in text_lower:
        return "Learning"
    elif "mood" in text_lower or "sad" in text_lower or "happy" in text_lower:
        return "Mood logs"
    elif "goal" in text_lower or "dream" in text_lower:
        return "Life goals"
    elif "improve" in text_lower or "sudhar" in text_lower:
        return "Improvement notes"
    elif "voice" in text_lower:
        return "Voice logs"
    elif "quote" in text_lower:
        return "Quotes"
    elif "reminder" in text_lower:
        return "Reminders"
    elif "task" in text_lower and "done" in text_lower:
        return "Task done"
    elif "journal" in text_lower or "diary" in text_lower:
        return "Daily journal"
    elif "anibook" in text_lower or "chapter" in text_lower:
        return "Anibook outline"
    elif "fact" in text_lower:
        return "User facts"
    elif "backup" in text_lower:
        return "Auto backup logs"
    else:
        return "Memory"

# 💾 Save logic
if submit and text_input:
    tab = detect_tab(text_input)
    ws = spreadsheet.worksheet(tab)
    headers = ws.row_values(1)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Generate row based on tab format
    row = []
    for col in headers:
        if col == "Date" or col == "DateTime":
            row.append(now)
        elif col == "User":
            row.append(user)
        else:
            row.append(text_input)
    ws.append_row(row)
    st.success(f"✅ Saved to **{tab}** tab for user **{user}**.")
