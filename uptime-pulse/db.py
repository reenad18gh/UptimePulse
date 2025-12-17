import sqlite3
from datetime import datetime

DB_NAME = "uptimepulse.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS status_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            reason TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_status(status: str, reason: str = ""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO status_log (timestamp, status, reason) VALUES (?, ?, ?)",
        (datetime.utcnow().isoformat(), status, reason),
    )

    conn.commit()
    conn.close()


def get_last_status():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM status_log ORDER BY id DESC LIMIT 1"
    )
    row = cur.fetchone()

    conn.close()
    return row[0] if row else None
