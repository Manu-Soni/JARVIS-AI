
# ==========================================
# PROJECT: J.A.R.V.I.S.
# DAY 3: Voice Enabled Assistant
# ==========================================

from datetime import datetime
import subprocess

# JARVIS SPEAKING FUNCTION
def speak(text):
    print("JARVIS:", text)

    safe_text = text.replace("'", "''")

    powershell_script = f"""
    Add-Type -AssemblyName System.Speech
    $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voice.Rate = 0
    $voice.Volume = 100
    $voice.Speak('{safe_text}')
    $voice.Dispose()
    """

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", powershell_script],
        check=False,
        creationflags=subprocess.CREATE_NO_WINDOW
    )


# INTRODUCTION
def introduce_jarvis():
    print("=" * 45)
    print("       J.A.R.V.I.S. AI ASSISTANT")
    print("=" * 45)

    speak("Hello! I am online. How can I help you?")


# COMMAND PROCESSOR
def process_command(command):

    if command == "hello":
        speak("Hello! Nice to see you.")

    elif command == "how are you":
        speak("All systems are working perfectly!")

    elif command == "who are you":
        speak("I am JARVIS, your personal AI assistant.")

    elif command == "what is your name":
        speak("My name is JARVIS!")

    elif command == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif command == "date":
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}.")

    elif command == "help":
        speak("Here are your available commands.")
        print("hello")
        print("how are you")
        print("who are you")
        print("what is your name")
        print("time")
        print("date")
        print("help")
        print("exit")

    elif command == "exit":
        speak("Shutting down. Goodbye!")
        return False

    else:
        speak("Sorry, I don't understand that command yet.")

    return True


# MAIN PROGRAM
def main():

    introduce_jarvis()

    running = True

    while running:
        command = input("You: ").lower().strip()
        running = process_command(command)


if __name__ == "__main__":
    main()
