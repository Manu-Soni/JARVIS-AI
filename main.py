
# ==========================================
# PROJECT: J.A.R.V.I.S.
# DAY 4: Voice Recognition Enabled Assistant
# ==========================================

from datetime import datetime
import subprocess
import speech_recognition as sr


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

    command = command.lower().strip()

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


# VOICE RECOGNITION
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nJARVIS: Listening...")

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=7
        )

    try:
        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("YOU:", command)
        return command.lower().strip()

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please repeat.")
        return ""

    except sr.RequestError:
        speak("Speech service unavailable. Please check your internet.")
        return ""


# MAIN PROGRAM
def main():

    introduce_jarvis()

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            speak("Please wait. Calibrating microphone.")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            speak("Microphone ready. You can speak now.")

            running = True

            while running:

                print("\nJARVIS: Say a command...")

                try:
                    audio = recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=7
                    )

                    command = recognizer.recognize_google(
                        audio,
                        language="en-IN"
                    )

                    print("YOU:", command)

                    running = process_command(command)

                except sr.WaitTimeoutError:
                    print("JARVIS: No speech detected. Listening again...")

                except sr.UnknownValueError:
                    speak("Sorry, I couldn't understand. Please repeat.")

                except sr.RequestError:
                    speak("Speech service unavailable. Check your internet.")

    except OSError as error:
        print("JARVIS: Microphone problem:", error)
        speak("I cannot access the microphone.")


if __name__ == "__main__":
    main()
