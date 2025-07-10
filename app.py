# [app.py code here — main UI code]
# NOTE: I'll give full app.py code again if needed
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
try:
    sheet = client.open("AniGPT_DB")
except Exception as e:
    st.error(f"❌ Sheet open error: {e}")
    st.stop()


# Save functions
def save_to_memory(prompt, response):
    sheet.worksheet("Memory").append_row([prompt, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def save_mood(mood, trigger=""):
    sheet.worksheet("MoodLogs").append_row([datetime.now().strftime("%Y-%m-%d"), mood, trigger])

def add_to_journal(summary, keywords=""):
    sheet.worksheet("DailyJournal").append_row([datetime.now().strftime("%Y-%m-%d"), summary, keywords])

def add_learning(learning, context=""):
    sheet.worksheet("Learnings").append_row([datetime.now().strftime("%Y-%m-%d"), learning, context])

def add_reminder(task, date, time, status="Pending"):
    sheet.worksheet("Reminders").append_row([task, date, time, status])

def add_goal(goal, category, deadline, progress="Not Started"):
    sheet.worksheet("LifeGoals").append_row([goal, category, deadline, progress])

# UI
st.set_page_config(page_title="AniGPT - Emotional AI", layout="centered")
st.title("🤖 AniGPT - Emotional & Self-Learning AI")
st.markdown("Jitna tu bolega, utna main yaad rakhunga 💡")

# Prompt Input
st.subheader("💬 Ask Something:")
prompt = st.text_input("You:", placeholder="Mujhse kuch bhi poochho...")

if prompt:
    response = f"AniGPT ka jawaab: '{prompt[::-1]}' 😄"  # Dummy reverse logic
    st.success(response)
    save_to_memory(prompt, response)

# Mood
st.subheader("😊 How Are You Feeling?")
mood = st.selectbox("Mood", ["Happy", "Sad", "Neutral", "Excited", "Tired", "Angry"])
trigger = st.text_input("Trigger / Reason", placeholder="Mood ka reason likho...")
if st.button("Save Mood"):
    save_mood(mood, trigger)
    st.success("Mood saved!")

# Journal
st.subheader("📓 Daily Journal")
journal = st.text_area("Write your thoughts for today...")
keywords = st.text_input("Keywords (optional)")
if st.button("Save Journal"):
    add_to_journal(journal, keywords)
    st.success("Journal saved!")

# Learning
st.subheader("📘 What AniGPT Learned Today")
learning = st.text_input("New learning for AniGPT")
context = st.text_input("Context")
if st.button("Add Learning"):
    add_learning(learning, context)
    st.success("Learning saved!")

# Reminder
st.subheader("⏰ Add Reminder")
task = st.text_input("Reminder Task")
rem_date = st.date_input("Date")
rem_time = st.time_input("Time")
if st.button("Add Reminder"):
    add_reminder(task, rem_date.strftime("%Y-%m-%d"), rem_time.strftime("%H:%M"))
    st.success("Reminder added!")

# Life Goals
st.subheader("🎯 Life Goal Tracker")
goal = st.text_input("Your Goal")
category = st.text_input("Goal Category (Health, Career, etc.)")
deadline = st.date_input("Target Date")
if st.button("Add Goal"):
    add_goal(goal, category, deadline.strftime("%Y-%m-%d"))
    st.success("Goal saved!")

st.markdown("---")
st.markdown("🔒 All your data is stored in your private Google Sheet.")
