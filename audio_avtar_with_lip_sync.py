import pygame
import time
import threading
from pygame import mixer
import pyttsx3
from gtts import gTTS
import os
from global_variables import audio_done
import pyaudio
import numpy as np

# Set up audio input
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


# Define thresholds for mouth movement based on audio volume
VOLUME_THRESHOLDS = {
    "neutral": 200,
    "open": 2000,
    "wide": 2500,
}


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def text_to_speech_gtts(text, filename="output_lipsync.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    #os.system(f"start {filename}")



avatar_image = pygame.image.load('avatar.png')
avatar = pygame.transform.scale(avatar_image, (200, 200))

# mouth_shapes = {
#     'open': pygame.transform.scale(pygame.image.load('mouth_open.png'),(200, 200)),
#     'smile': pygame.transform.scale(pygame.image.load('mouth_round.png'),(200, 200)),
#     'closed': pygame.transform.scale(pygame.image.load('mouth_closed.png'),(200, 200)),
#     'neutral': pygame.transform.scale(pygame.image.load('mouth_closed.png'),(200, 200)),
#     'teeth': pygame.transform.scale(pygame.image.load('mouth_open.png'),(200, 200)),
#     'tight': pygame.transform.scale(pygame.image.load('mouth_closed.png'),(200, 200))
# }

mouth_shapes = {
    'open': pygame.transform.scale(pygame.image.load('mouth_open.png'),(200, 200)),
    'smile': pygame.transform.scale(pygame.image.load('mouth_round.png'),(200, 200)),
    'closed': pygame.transform.scale(pygame.image.load('mouth_closed.png'),(200, 200)),
    'neutral': pygame.transform.scale(pygame.image.load('mouth_closed.png'),(200, 200)),
    'teeth': pygame.transform.scale(pygame.image.load('mouth_open.png'),(200, 200)),
    'tight': pygame.transform.scale(pygame.image.load('mouth_closed.png'),(200, 200))
}


# Function to play audio
def play_audio(filename):
    mixer.music.load(filename)
    mixer.music.play()
    audio_done.set()


def play_audio_with_pyttsx3_nonblocking(text):
    """Play text using pyttsx3 without blocking other threads."""

    def speak():
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Speed of speech
        engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)
        #engine.setProperty('voice', 2.0)

        print("Speaking...")
        engine.say(text)
        engine.runAndWait()  # Synthesize and play the audio
        engine.stop()
        print("Audio done.")
        audio_done.set()  # Mark audio as completed

    # Run pyttsx3 in a separate thread
    speak_thread = threading.Thread(target=speak)
    speak_thread.start()

# Function to render avatar with lip-sync
def run_avatar_animation(screen,stream):
    """Simulate avatar animation during speech."""
    frame = 0
    print("Starting avatar animation...")

    while not audio_done.is_set():  # Run until audio finishes

        # Read audio data
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        volume = np.abs(data).mean()  # Calculate average volume

        # Determine mouth shape based on volume
        if volume < VOLUME_THRESHOLDS["neutral"]:
            mouth_shape = mouth_shapes["neutral"]
        elif volume < VOLUME_THRESHOLDS["open"]:
            mouth_shape = mouth_shapes["open"]
        else:
            mouth_shape = mouth_shapes["smile"]

        # Clear screen and render avatar
        screen.fill((255, 255, 255))
        screen.blit(avatar, (50, 25))
        screen.blit(mouth_shape, (50, 25))  # Adjust mouth position
        # screen.blit(rendered_text, (20,250))

        pygame.display.flip()

        time.sleep(0.05)  # Simulate rendering delay
        frame += 1

    print("Avatar animation finished.")


def tts_with_lipsync_2(text,language):


    #text_to_speech_gtts(text)
    pygame.init()
    mixer.init()

    ## Set up stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Set up display
    screen = pygame.display.set_mode((300, 300))
    #font = pygame.font.Font(None, 18)
    #rendered_text = font.render(text, True, (0, 0, 0))

    audio_done.clear()
    pygame.display.set_caption("Avatar Lip-Sync")

    # Start audio playback in a separate thread
    audio_thread = threading.Thread(target=play_audio_with_pyttsx3_nonblocking, args=(text,))
    #audio_thread = threading.Thread(target=play_audio, args=("output_lipsync.mp3",))
    #avatar_thread = threading.Thread(target=run_avatar_animation, args=(screen, phoneme_timings,))
    avatar_thread = threading.Thread(target=run_avatar_animation, args=(screen,stream,))

    # Start both threads
    audio_thread.start()
    avatar_thread.start()

    # Wait for both threads to finish
    audio_thread.join()
    avatar_thread.join()

    print("Program finished.")
    mixer.quit()
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()



# Example usage
# if __name__ == "__main__":
#     tts_with_lipsync("Hello, how are you today? My name is Radha")