import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fba_memory.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT,
                        response TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
        conn.commit()

init_db()

def save_interaction(question, response):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO memory (question, response) VALUES (?, ?)", (question, response))
        conn.commit()

def get_last_interactions(limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT question, response FROM memory ORDER BY created_at DESC LIMIT ?", (limit,))
        return c.fetchall()