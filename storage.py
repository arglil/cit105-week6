import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "data" / "boards.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def load_data():
    return {
        "boards": get_boards(),
        "cards": get_cards()
    }


def save_data(data):
    with get_connection() as conn:
        conn.execute("DELETE FROM cards")
        conn.execute("DELETE FROM boards")

        for board in data["boards"]:
            conn.execute(
                "INSERT INTO boards (id, name) VALUES (?, ?)",
                (board["id"], board["name"])
            )

        for card in data["cards"]:
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


def get_boards():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name FROM boards ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


def get_cards(board_id=None):
    with get_connection() as conn:
        if board_id is None:
            rows = conn.execute(
                "SELECT id, board_id, title, priority FROM cards ORDER BY id"
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, board_id, title, priority
                FROM cards
                WHERE board_id = ?
                ORDER BY id
                """,
                (board_id,)
            ).fetchall()

        return [dict(row) for row in rows]


def add_board(name):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO boards (name) VALUES (?)",
            (name,)
        )
        return {"id": cursor.lastrowid, "name": name}


def add_card(board_id, title, priority="medium"):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO cards (board_id, title, priority)
            VALUES (?, ?, ?)
            """,
            (board_id, title, priority)
        )

        return {
            "id": cursor.lastrowid,
            "board_id": board_id,
            "title": title,
            "priority": priority
        }