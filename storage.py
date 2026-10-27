
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "boards.json"


def load_data():
    if not DATA_FILE.exists():
        return {"boards": [], "cards": []}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_boards():
    return load_data()["boards"]


def get_cards(board_id=None):
    cards = load_data()["cards"]

    if board_id is not None:
        cards = [
            card for card in cards
            if card["board_id"] == board_id
        ]

    return cards


def add_board(name):
    data = load_data()

    board = {
        "id": max(
            [b["id"] for b in data["boards"]],
            default=0
        ) + 1,
        "name": name
    }

    data["boards"].append(board)
    save_data(data)
    return board


def add_card(board_id, title, priority="medium"):
    data = load_data()

    card = {
        "id": max(
            [c["id"] for c in data["cards"]],
            default=0
        ) + 1,
        "board_id": board_id,
        "title": title,
        "priority": priority
    }

    data["cards"].append(card)
    save_data(data)
    return card
