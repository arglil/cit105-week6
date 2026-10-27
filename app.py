
from storage import get_boards, get_cards, add_board, add_card


def main():
    boards = get_boards()

    if not boards:
        add_board("IT Projects")
        add_board("School Assignments")

    boards = get_boards()

    if not get_cards():
        add_card(1, "Complete SQLite migration", "high")
        add_card(1, "Review database constraints", "medium")
        add_card(2, "Submit Week 6 assignment", "high")

    print("\nBOARDS AND CARDS")
    print("================")

    for board in get_boards():
        print(f"\nBoard: {board['name']}")

        for card in get_cards(board["id"]):
            print(
                f"  - {card['title']} "
                f"[{card['priority']}]"
            )


if __name__ == "__main__":
    main()
