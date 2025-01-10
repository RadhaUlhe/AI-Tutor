import threading

# Define global variables here
audio_done = threading.Event()  # Thread-safe event


# import pyttsx3
#
# if __name__=="__main__":
#     #text = "यह एक परीक्षण है।"
#     text = "i m radha"
#     engine = pyttsx3.init()
#     engine.setProperty("rate", 150)
#     engine.setProperty("volume", 1.0)
#
#     # Use the default voice (if no Hindi-specific voice is available)
#     engine.say(text)
#     engine.runAndWait()


