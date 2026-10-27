import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "data" / "boards.db"

def initialize_database():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("PRAGMA foreign_keys = ON")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS boards (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK (length(trim(name)) > 0)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                board_id INTEGER NOT NULL,
                title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                priority TEXT NOT NULL DEFAULT 'medium'
                    CHECK (priority IN ('low', 'medium', 'high')),
                FOREIGN KEY (board_id) REFERENCES boards(id)
            )
        """)

        conn.commit()
        print("SQLite database initialized successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()