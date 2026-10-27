import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_FILE = BASE / "data" / "boards.json"
DB_FILE = BASE / "data" / "boards.db"


def migrate():
    if not JSON_FILE.exists():
        print("JSON file not found. Migration stopped.")
        return

    with JSON_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    boards = data["boards"]
    cards = data["cards"]

    conn = sqlite3.connect(DB_FILE)

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        existing_boards = conn.execute(
            "SELECT COUNT(*) FROM boards"
        ).fetchone()[0]

        existing_cards = conn.execute(
            "SELECT COUNT(*) FROM cards"
        ).fetchone()[0]

        if existing_boards or existing_cards:
            print("Database already contains data. Migration stopped.")
            return

        with conn:
            for board in boards:
                conn.execute(
                    "INSERT INTO boards (id, name) VALUES (?, ?)",
                    (board["id"], board["name"])
                )

            for card in cards:
                conn.execute(
                    """
                    INSERT INTO cards (id, board_id, title, priority)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        card["id"],
                        card["board_id"],
                        card["title"],
                        card["priority"]
                    )
                )

        db_boards = conn.execute(
            "SELECT COUNT(*) FROM boards"
        ).fetchone()[0]

        db_cards = conn.execute(
            "SELECT COUNT(*) FROM cards"
        ).fetchone()[0]

        assert db_boards == len(boards)
        assert db_cards == len(cards)

        print("Migration completed successfully!")
        print(f"Boards migrated: {db_boards}")
        print(f"Cards migrated: {db_cards}")

    finally:
        conn.close()


if __name__ == "__main__":
    migrate()