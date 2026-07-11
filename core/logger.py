import sqlite3
import datetime
import os

DB_FILE = "logs.db"

def init_db():
    """Initializes the SQLite database with the necessary table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT NOT NULL,
            overall_risk_score TEXT NOT NULL,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_analysis(filename: str, overall_risk_score: str, details: str = ""):
    """Logs a single analysis event to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO analysis_logs (timestamp, filename, overall_risk_score, details) VALUES (?, ?, ?, ?)",
        (timestamp, filename, overall_risk_score, details)
    )
    
    conn.commit()
    conn.close()

# Initialize the database when the module is loaded
init_db()
