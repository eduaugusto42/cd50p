WORDS = {"PAIR": 4, "HAIR": 4, "CHAIR": 5, "GRAPHIC": 7}

def main():
    print("Welcome to the Spelling Bee!")

    while len(WORDS) > 0:
        print(f"{len(WORDS)} words left!")
        guess = input("Guess a word: ")

        # Check if guess in dictionary
        if guess == "GRAPHIC":
            WORDS.clear()
            print("You've won!")

        elif guess in WORDS.keys():
            points = WORDS.pop(guess)
            print(f"Good job! You scored {points} points.")

    print("That's the game!")


main()