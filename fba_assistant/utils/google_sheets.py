import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sqlite3

def export_to_csv():
    sheet_id = os.getenv("GSPREAD_SHEET_ID")
    worksheet_name = os.getenv("GSPREAD_WORKSHEET_NAME", "Feuille1")
    if not sheet_id:
        return "❌ Aucun identifiant Google Sheets trouvé."

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)

    sh = client.open_by_key(sheet_id)
    worksheet = sh.worksheet(worksheet_name)

    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "fba_memory.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT question, response FROM memory ORDER BY created_at DESC LIMIT 50")
    rows = c.fetchall()

    worksheet.clear()
    worksheet.append_row(["Question", "Réponse"])
    for row in rows:
        worksheet.append_row(list(row))

    return "✅ Export terminé vers Google Sheets"