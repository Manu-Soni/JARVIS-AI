
# =====================================
# PROJECT: J.A.R.V.I.S.
# DAY 2: Interactive Assistant
# =====================================

from datetime import datetime


def introduce_jarvis():
    print("=" * 45)
    print("       J.A.R.V.I.S. AI ASSISTANT")
    print("=" * 45)

    print("JARVIS: Hello Manu! I am online.")
    print("JARVIS: How can I help you?")
    print()


def process_command(command):

    if command == "hello":
        print("JARVIS: Hello Manu! Nice to see you.")

    elif command == "how are you":
        print("JARVIS: All systems are working perfectly!")

    elif command == "who are you":
        print("JARVIS: I am JARVIS, your personal AI assistant.")

    elif command == "what is your name":
        print("JARVIS: My name is JARVIS!")

    elif command == "time":
        current_time = datetime.now().strftime("%I:%M:%S %p")
        print(f"JARVIS: The current time is {current_time}.")

    elif command == "date":
        current_date = datetime.now().strftime("%d %B %Y")
        print(f"JARVIS: Today's date is {current_date}.")

    elif command == "help":
        print("JARVIS: Available commands:")
        print("- hello")
        print("- how are you")
        print("- who are you")
        print("- what is your name")
        print("- time")
        print("- date")
        print("- help")
        print("- exit")

    elif command == "exit":
        print("JARVIS: Shutting down. Goodbye Manu!")
        return False

    else:
        print("JARVIS: Sorry, I don't understand that command yet.")

    return True


def main():
    introduce_jarvis()

    running = True

    while running:
        command = input("You: ").lower().strip()
        running = process_command(command)


if __name__ == "__main__":
    main()
