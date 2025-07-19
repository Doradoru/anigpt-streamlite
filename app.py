import streamlit as st
import gspread
from datetime import datetime
import json
from google.oauth2.service_account import Credentials

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="AniGPT v2.0", page_icon="🧠")

st.title("🧠 AniGPT v2.0 – Personal Smart Logger")

# ------------------- SECRETS SETUP ------------------
json_key = st.secrets["GOOGLE_SHEET_JSON"]
json_data = json.loads(json_key)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(json_data, scopes=scopes)

gc = gspread.authorize(credentials)

# ----------------- CONNECT TO SHEET -----------------
SHEET_NAME = "AniGPT_DB"

try:
    sh = gc.open(SHEET_NAME)
except Exception as e:
    st.error(f"❌ Failed to open sheet: {e}")
    st.stop()

# ------------------ SHEET TABS ----------------------
REQUIRED_TABS = {
    "Memory": ["Date", "User", "Memory"],
    "Mood logs": ["Date", "User", "Mood", "Trigger"],
    "Daily journal": ["Date", "User", "Summary", "Keywords"],
    "Learning": ["Date", "User", "WhatWasLearned", "Context"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "User", "Transcript"],
    "Anibook outline": ["Chapter", "Idea", "User"],
    "Improvement notes": ["Date", "User", "Note"],
    "Quotes": ["Quote", "By", "User"],
    "User facts": ["Fact", "User"],
    "Task done": ["Task", "Date", "User"],
    "Auto backup logs": ["Timestamp", "Details", "User"]
}

# ---------------- AUTO TAB + HEADER CREATOR ---------
def ensure_tabs():
    existing_tabs = [ws.title for ws in sh.worksheets()]
    for tab, headers in REQUIRED_TABS.items():
        if tab not in existing_tabs:
            ws = sh.add_worksheet(title=tab, rows=100, cols=len(headers))
            ws.append_row(headers)
        else:
            ws = sh.worksheet(tab)
            current_headers = ws.row_values(1)
            for h in headers:
                if h not in current_headers:
                    ws.update_cell(1, len(current_headers) + 1, h)
                    current_headers.append(h)

ensure_tabs()

# ---------------------- UI --------------------------

st.subheader("🧑 Select User")
user = st.selectbox("Who is using AniGPT?", ["Ani", "Anne"])

input_text = st.text_area("📝 Enter your message (memory, mood, journal...)", height=150)

submit = st.button("💾 Save to Google Sheet")

# --------------------- SAVE LOGIC -------------------

if submit and input_text.strip():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")

    detected = False

    for tab, headers in REQUIRED_TABS.items():
        if any(h.lower() in input_text.lower() for h in headers if h not in ["User", "Date"]):
            row = []
            for h in headers:
                if h == "Date":
                    row.append(date_str)
                elif h == "User":
                    row.append(user)
                else:
                    row.append(input_text)
            ws = sh.worksheet(tab)
            ws.append_row(row)
            st.success(f"✅ Saved to `{tab}`!")
            detected = True
            break

    if not detected:
        st.warning("⚠️ Could not detect category from input. Please be specific (like 'mood', 'quote', 'task').")

