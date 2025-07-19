import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="AniGPT v2", layout="centered")
st.title("🧠 AniGPT v2 – Auto Tab Detection AI")

# Load credentials from secrets
json_key = st.secrets["GOOGLE_SHEET_JSON"]
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(json_key, scopes=scope)
gc = gspread.authorize(credentials)

# Open the sheet
SHEET_NAME = "AniGPT_DB"
try:
    sheet = gc.open(SHEET_NAME)
except Exception as e:
    st.error(f"❌ Failed to open sheet: {e}")
    st.stop()

# Tab detection function
def detect_tab(text):
    text = text.lower()
    if any(word in text for word in ["sad", "happy", "angry", "depressed", "joy", "tired"]):
        return "Mood logs"
    elif any(word in text for word in ["learn", "sikh", "understand", "studied", "coding"]):
        return "Learning"
    elif any(word in text for word in ["goal", "target", "mission", "aim"]):
        return "Life goals"
    elif any(word in text for word in ["journal", "summary", "din", "routine"]):
        return "Daily journal"
    elif any(word in text for word in ["voice", "mic", "recorded"]):
        return "Voice logs"
    elif any(word in text for word in ["task", "kaam", "done", "complete"]):
        return "Task done"
    elif any(word in text for word in ["note", "habit", "improve"]):
        return "Improvement notes"
    elif any(word in text for word in ["quote", "motivation", "line"]):
        return "Quotes"
    elif any(word in text for word in ["anne", "ani", "me", "facts", "truth"]):
        return "User facts"
    elif any(word in text for word in ["backup", "sync", "auto"]):
        return "Auto backup logs"
    elif any(word in text for word in ["chapter", "book", "outline"]):
        return "Anibook outline"
    elif any(word in text for word in ["remind", "yaad dilao", "tomorrow", "reminder"]):
        return "Reminders"
    else:
        return "Memory"

# Ensure tab exists and has User column
def ensure_tab(tab_name):
    try:
        ws = sheet.worksheet(tab_name)
    except:
        ws = sheet.add_worksheet(title=tab_name, rows="100", cols="10")
        ws.append_row(["Date", "User", "Content"])
    return ws

# User selector
user = st.selectbox("👤 Select user", ["Ani", "Anne"])

# Input form
with st.form("data_entry_form"):
    user_input = st.text_area("📝 Write something...", height=150)
    submit = st.form_submit_button("💾 Save Entry")

if submit and user_input:
    tab = detect_tab(user_input)
    ws = ensure_tab(tab)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ws.append_row([now, user, user_input])
    st.success(f"✅ Saved to '{tab}' for {user}")
