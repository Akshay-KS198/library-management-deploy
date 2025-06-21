import os
import json
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

SHEET_NAME = "LibraryBooks"
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON")

if not GOOGLE_CREDS_JSON:
    raise ValueError("Missing GOOGLE_CREDS_JSON environment variable")

service_account_info = json.loads(GOOGLE_CREDS_JSON)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

def get_all_books():
    return sheet.get_all_records()

def add_book(book, availability):
    if availability > 0:
        sheet.append_row([book, availability])
        return True 
    return False

def update_book(book, new_count):
    if new_count < 0:
        return False
    records = sheet.get_all_records()
    for idx, record in enumerate(records, start=2):
        if record['Book'] == book:
            sheet.update_cell(idx, 2, new_count)
            return True
    return False

def delete_book(book):
    records = sheet.get_all_records()
    for idx, record in enumerate(records, start=2):
        if record['Book'] == book:
            sheet.delete_rows(idx)
            return True
    return False

