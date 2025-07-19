import gspread
from google.oauth2.service_account import Credentials

# Load credentials
json_key = {
    # Paste your JSON credentials here (shortened for this example)
}

# Sheet and tab structure
sheet_name = "AniGPT_DB"

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

# Authenticate
creds = Credentials.from_service_account_info(json_key, scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Open or create sheet
spreadsheet = client.open(sheet_name)

# Ensure each tab and heading exists
for tab_name, headers in tabs_with_headings.items():
    try:
        ws = spreadsheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=tab_name, rows="100", cols="20")
        print(f"✅ Created tab: {tab_name}")
    
    existing_headers = ws.row_values(1)
    if existing_headers != headers:
        ws.resize(rows=100, cols=len(headers))  # Adjust columns
        ws.delete_rows(1)  # Remove existing header
        ws.insert_row(headers, index=1)
        print(f"✅ Updated headers in tab: {tab_name}")
    else:
        print(f"✔️ Headers already correct in: {tab_name}")
