import streamlit as st
import gspread
from datetime import datetime
import json
from google.oauth2.service_account import Credentials
import pandas as pd

# ---- AUTH ----
json_key = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(credentials)

# ---- SHEET INFO ----
SHEET_NAME = "AniGPT_DB"
try:
    sheet = client.open(SHEET_NAME)
except Exception as e:
    st.error(f"❌ Failed to open sheet: {e}")
    st.stop()

# ---- TAB METADATA ----
tab_info = {
    "Memory": ["yaad", "remember", "past", "old", "nostalgia"],
    "Mood logs": ["happy", "sad", "angry", "mood", "tension", "frustrated"],
    "Daily journal": ["aaj", "today", "diary", "journal", "routine"],
    "Learning": ["learn", "padhai", "study", "python", "course", "sikha"],
    "Reminders": ["remind", "yaad dilao", "kal", "appointment", "task"],
    "Life goals": ["goal", "target", "sapna", "dream", "future"],
    "Voice logs": ["voice", "audio", "record", "bolkar"],
    "Anibook outline": ["book", "chapter", "outline", "summary"],
    "Improvement notes": ["improve", "habit", "change", "better"],
    "Quotes": ["quote", "saying", "kahavat", "inspiration"],
    "User facts": ["ani", "anne", "pasand", "dislike", "favourite"],
    "Task done": ["complete", "done", "kaam khatam", "finished"],
    "Auto backup logs": ["backup", "auto", "saved", "sync"]
}

# ---- UI ----
st.title("🧠 AniGPT v2.0 – Personal Dashboard")
user = st.selectbox("👤 Select User", ["Ani", "Anne"])
user_input = st.text_area("📝 Type your message below:")
submit = st.button("💾 Save Entry")

# ---- TAB DETECTION FUNCTION ----
def detect_tab(text):
    text_lower = text.lower()
    for tab, keywords in tab_info.items():
        for kw in keywords:
            if kw in text_lower:
                return tab
    return "Memory"  # fallback

# ---- ENSURE REQUIRED COLUMNS EXIST ----
def ensure_headers(tab, headers):
    try:
        worksheet = sheet.worksheet(tab)
    except:
        worksheet = sheet.add_worksheet(title=tab, rows="100", cols="20")
    existing_headers = worksheet.row_values(1)
    for i, h in enumerate(headers):
        if h not in existing_headers:
            worksheet.update_cell(1, len(existing_headers) + 1, h)
            existing_headers.append(h)

# ---- SUBMIT LOGIC ----
if submit and user_input.strip():
    tab = detect_tab(user_input)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data_row = []
    if tab == "Mood logs":
        headers = ["Date", "Mood", "Trigger", "User"]
        mood = "Happy" if "happy" in user_input.lower() else "Unknown"
        trigger = user_input[:30]
        data_row = [date_str, mood, trigger, user]
    elif tab == "Daily journal":
        headers = ["Date", "Summary", "Keywords", "User"]
        data_row = [date_str, user_input, "auto", user]
    elif tab == "Learning":
        headers = ["Date", "WhatWasLearned", "Context", "User"]
        data_row = [date_str, user_input, "auto", user]
    elif tab == "Reminders":
        headers = ["Task", "Date", "Time", "Status", "User"]
        data_row = [user_input, date_str.split()[0], date_str.split()[1], "Pending", user]
    elif tab == "Life goals":
        headers = ["Goal", "Category", "Target Date", "Progress", "User"]
        data_row = [user_input, "Personal", "N/A", "0%", user]
    elif tab == "Voice logs":
        headers = ["Date", "Note", "User"]
        data_row = [date_str, user_input, user]
    elif tab == "Anibook outline":
        headers = ["Chapter", "Summary", "User"]
        data_row = ["Auto", user_input, user]
    elif tab == "Improvement notes":
        headers = ["Date", "Note", "User"]
        data_row = [date_str, user_input, user]
    elif tab == "Quotes":
        headers = ["Quote", "Author", "User"]
        data_row = [user_input, "Unknown", user]
    elif tab == "User facts":
        headers = ["Fact", "User"]
        data_row = [user_input, user]
    elif tab == "Task done":
        headers = ["Task", "Status", "Date", "User"]
        data_row = [user_input, "Done", date_str, user]
    elif tab == "Auto backup logs":
        headers = ["Log", "Time", "User"]
        data_row = [user_input, date_str, user]
    else:
        headers = ["Date", "Memory", "User"]
        data_row = [date_str, user_input, user]

    # Ensure tab and headers
    ensure_headers(tab, headers)
    worksheet = sheet.worksheet(tab)
    worksheet.append_row(data_row)
    st.success(f"✅ Entry saved to '{tab}' tab.")

