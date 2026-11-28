
# ==========================================
# PROJECT: J.A.R.V.I.S.
# DAY 4: Voice Recognition Enabled Assistant
# ==========================================

from datetime import datetime
import subprocess
import speech_recognition as sr
import webbrowser
from urllib.parse import quote_plus
import psutil
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


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


# BROWSER CONTROL
def open_website(website):
    webbrowser.open(website)



# APPLICATION CONTROL
def open_application(app_name):

    if app_name == "notepad":
        subprocess.Popen(["notepad.exe"])

    elif app_name == "calculator":
        subprocess.Popen(["calc.exe"])

    elif app_name == "vscode":
        vscode_path = r"C:\Users\Asus\AppData\Local\Programs\Microsoft VS Code\Code.exe"

        subprocess.Popen([vscode_path])

# SYSTEM VOLUME CONTROL

def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.10, 1.0)

    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak("Volume increased.")

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - 0.10, 0.0)

    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak("Volume decreased.")

def mute_volume():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume

    volume.SetMute(1, None)
    speak("Volume muted.")

def unmute_volume():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume

    volume.SetMute(0, None)
    speak("Volume unmuted.")

def check_volume():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume

    current_volume = volume.GetMasterVolumeLevelScalar()
    volume_percent = round(current_volume * 100)

    speak(f"The current volume is {volume_percent} percent.")
    


# BATTERY STATUS
def battery_status():

    battery = psutil.sensors_battery()

    if battery is None:
        speak("Sorry, I cannot detect a battery.")
        return

    percentage = battery.percent

    if battery.power_plugged:
        speak(f"Your laptop is plugged in. Battery is at {percentage} percent.")
    else:
        speak(f"Your laptop battery is at {percentage} percent.")


# INTRODUCTION
def introduce_jarvis():
    print("=" * 45)
    print("       J.A.R.V.I.S. AI ASSISTANT")
    print("=" * 45)

    speak("Hello! I am online. How can I help you?")



# ==========================================
# SMART COMMAND PROCESSOR
# DAY 7
# ==========================================

def get_brightness():
    command = (
        "(Get-CimInstance -Namespace root/WMI "
        "-ClassName WmiMonitorBrightness).CurrentBrightness"
    )

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True
    )

    if result.returncode != 0 or not result.stdout.strip():
        speak("Sorry, I couldn't read the brightness.")
        return None

    return int(result.stdout.strip())


def set_brightness(level):
    level = max(0, min(100, level))

    command = (
        "$monitor = Get-CimInstance -Namespace root/WMI "
        "-ClassName WmiMonitorBrightnessMethods; "
        f"Invoke-CimMethod -InputObject $monitor "
        f"-MethodName WmiSetBrightness "
        f"-Arguments @{{ Timeout = 1; Brightness = {level} }}"
    )

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        speak(f"Brightness set to {level} percent.")
    else:
        speak("Sorry, I couldn't change the brightness.")


def increase_brightness():
    current = get_brightness()
    if current is not None:
        set_brightness(min(100, current + 10))


def decrease_brightness():
    current = get_brightness()
    if current is not None:
        set_brightness(max(0, current - 10))


def check_brightness():
    current = get_brightness()
    if current is not None:
        speak(f"Brightness is at {current} percent.")

def process_command(command):

    command = command.lower().strip()

    # Remove JARVIS wake word
    command = command.replace("jarvis", "", 1).strip(" ,.!?")

    # Remove leftover "jar" from speech recognition
    if command.endswith(" jar"):
        command = command[:-4].strip()

    # Remove common polite phrases
    prefixes = [
        "hey can you ",
        "can you ",
        "could you ",
        "would you ",
        "please ",
        "tell me ",
        "hey "
    ]

    # Keep removing prefixes until none match
    while True:
        found = False

        for prefix in prefixes:
            if command.startswith(prefix):
                command = command[len(prefix):].strip()
                found = True
                break

        if not found:
            break

    # GREETINGS


    if command in ["hello", "hi", "hey"]:
        speak("Hello! Nice to see you.")

    # CONVERSATION
    elif command in [
        "how are you",
        "how are you doing",
        "hows everything going",
        "how everything going",
        "house everything going",
        "are you doing okay",
        "are you doing ok",
        "are you okay",
        "are you ok",
        "how are things"
    ]:
        speak("All systems are working perfectly!")

    elif command in ["who are you", "what are you"]:
        speak("I am JARVIS, your personal AI assistant.")

    elif command in ["what is your name", "your name"]:
        speak("My name is JARVIS!")

    # TIME
    elif command in ["time", "what time is it", "tell me the time"]:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    # DATE
    elif command in ["date", "what is the date", "tell me the date", "today's date"]:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}.")

    # HELP
    elif command in ["help", "show commands", "what can you do"]:
        speak("Here are some things I can do.")

        print("\nAVAILABLE COMMANDS")
        print("------------------")
        print("Hello")
        print("How are you")
        print("What time is it")
        print("What is the date")
        print("Open Google")
        print("Open YouTube")
        print("Open ChatGPT")
        print("Search for something")
        print("Open Notepad")
        print("Open Calculator")
        print("Open VS Code")
        print("Battery status")
        print("Exit")
        print("Increase brightness")
        print("Decrease brightness")
        print("Check brightness")
        print("Set brightness to 50 percent")

    # EXIT
    elif command in ["exit", "quit", "shutdown jarvis", "stop"]:
        speak("Shutting down. Goodbye!")
        return False

    # WEBSITE CONTROL
    elif "google" in command:
        speak("Opening Google.")
        open_website("https://www.google.com")

    elif command in ["open youtube", "youtube"]:
        speak("Opening YouTube.")
        open_website("https://www.youtube.com")

    elif command in ["open chatgpt", "chatgpt"]:
        speak("Opening ChatGPT.")
        open_website("https://chatgpt.com")

    # GOOGLE SEARCH
    elif command.startswith("search for ") or command.startswith("search "):
        query = command.replace("search for ", "", 1)
        if query == command:
            query = command.replace("search ", "", 1)

        if query.strip():
            speak(f"Searching Google for {query}")
            search_url = "https://www.google.com/search?q=" + quote_plus(query)
            open_website(search_url)
        else:
            speak("What would you like me to search for?")

    # APPLICATION CONTROL
    elif command in ["open notepad", "start notepad", "launch notepad"]:
        speak("Opening Notepad.")
        open_application("notepad")

    elif command in ["open calculator", "start calculator", "launch calculator"]:
        speak("Opening Calculator.")
        open_application("calculator")

    elif command in [
        "open vscode",
        "open vs code",
        "open visual studio code",
        "start vscode",
        "launch vscode"
    ]:
        speak("Opening Visual Studio Code.")
        open_application("vscode")

    # BATTERY STATUS
    elif command in ["battery", "battery status", "check battery", "how much battery is left"]:
        battery_status()

    # UNKNOWN COMMAND
    # SYSTEM VOLUME CONTROL
    elif command in [
    "increase volume",
    "volume up",
    "raise volume"
]:
         increase_volume()

    elif command in [
    "decrease volume",
    "volume down",
    "lower volume"
]:
      decrease_volume()

    elif command in [
    "mute",
    "mute volume"
]:
     mute_volume()

    elif command in [
    "unmute",
    "unmute volume"
]:
     unmute_volume()

    elif command in [
        "check volume",
        "volume status",
        "what is the volume"
    ]:
        check_volume()

        # SCREEN BRIGHTNESS CONTROL
    elif command in ["increase brightness", "brightness up", "raise brightness"]:
        increase_brightness()

    elif command in ["decrease brightness", "brightness down", "lower brightness"]:
        decrease_brightness()

    elif command in ["check brightness", "brightness status", "what is the brightness"]:
        check_brightness()

    elif command.startswith("set brightness to "):
        value = command.replace("set brightness to ", "", 1)
        value = value.replace(" percent", "").strip()

        if value.isdigit():
            set_brightness(int(value))
        else:
            speak("Please tell me a brightness level from 0 to 100.")

# UNKNOWN COMMAND
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
        print("JARVIS: Microphone or audio device problem:", error)
        speak("There is a problem accessing the microphone.")


if __name__ == "__main__":
    main()
