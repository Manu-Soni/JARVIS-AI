
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

print("Starting voice test...")

engine.say("First voice test.")
engine.say("Second voice test.")
engine.say("Third voice test.")
engine.say("Fourth voice test.")

engine.runAndWait()

print("Voice test completed.")
