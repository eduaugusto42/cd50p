import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    # Format user input
    hours = re.search(r"^(9:00 AM) to (5:00 PM)", s)

    # Check group 1 and 2 for "AM" or "PM"
    # If "AM", check if hours = 12
        # Change hours to zero if is

    # If "PM", check if hours = 12
        # Do nothing if is
        # Add 12 to hours if isn't

    if hours:
        return "09:00 to 17:00"


if __name__ == "__main__":
    main()
