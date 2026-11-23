
import speech_recognition as sr

recognizer = sr.Recognizer()

print("JARVIS: Microphone test starting...")

with sr.Microphone(device_index=2) as source:
    print("JARVIS: Adjusting microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("JARVIS: Speak something now!")
    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

    print("JARVIS: Recording completed!")

try:
    text = recognizer.recognize_google(audio)
    print("YOU:", text)

except sr.UnknownValueError:
    print("JARVIS: Sorry, I couldn't understand.")

except sr.RequestError:
    print("JARVIS: Speech service unavailable. Check internet.")
