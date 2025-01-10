import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
#from playsound import playsound
from transformers import pipeline
from pydub import AudioSegment
from langchain_ollama import OllamaLLM
import os
import sys
import asyncio
AudioSegment.converter = "C:/Apps/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = "C:/Apps/ffmpeg/bin/ffprobe.exe"
from pydub.playback import play

#from lip_sync_audio_avtar import tts_with_lipsync, tts_with_lipsync_2
from audio_avtar_with_lip_sync import tts_with_lipsync_2


# Initialize components
recognizer = sr.Recognizer()
translator = Translator()
#ai_tutor = pipeline("text-generation", model="openlm-research/open_llama_3b")  # Replace with your fine-tuned model
llm = OllamaLLM(model="llama3.2")

def capture_voice():
    """Capture voice input and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Speech recognition service unavailable")
        return None

async def detect_language(text):
    """Detect the language of the input text."""
    detection = await(translator.detect(text))
    print(f"Detected language: {detection.lang}")
    return detection.lang

def get_llama_prompt(user_message, system_message=""):
  system_prompt = ""
  if system_message != "":
    system_prompt = (
      f"<|start_header_id|>system<|end_header_id|>\n\n{system_message}"
      f"<|eot_id|>"
    )
  prompt = (f"<|begin_of_text|>{system_prompt}"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_message}"
            f"<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
           )
  return prompt

async def generate_response(question, language):
    """Generate AI response and translate to target language."""
    #response = ai_tutor(question, max_length=100)[0]['generated_text']

    ## construct prompt ##
    system_prompt = f'''
        you are tutor called as "ai-guru" in schools. you want to help teachers and students to learn new things and give answer to their questions.
        if user asks question, you need to give answer very quickly and precisely but not in bullets format. If user wants explanation then only give explanation

        '''

    prompt = get_llama_prompt(question, system_prompt)

    response = llm.invoke(prompt)

    print(f"AI Response: {response}")
    return response
    # src_lang="en"
    # if language != "en":  # If not English, translate
    #     response = await translator.translate(response, src=src_lang, dest=language)
    # return response.text
    # except translator.raise_exception as e:
    #     print(f"Error: {e}")



def text_to_speech(text, language):
    """Convert text to speech."""
    tts = gTTS(text=text, lang=language)
    audio_file = "./response.mp3"
    tts.save(audio_file)
    audio = AudioSegment.from_file(audio_file, format="mp3")
    print("audio loaded!")
    play(audio)
    os.remove(audio_file)

# Main function
# def ai_tutor_voice():
#     while True:
#         question = capture_voice()
#         if question:
#             language = asyncio.run(detect_language(question))
#             response = asyncio.run(generate_response(question, language))
#             tts_with_lipsync(response)
#             # print(f"Translated Response: {response}")
#             # text_to_speech(response, language)

async def ai_tutor_voice():
    while True:
        question = capture_voice()
        if question:
            language = await detect_language(question)
            response = await generate_response(question, language)
            tts_with_lipsync_2(response,language)
            # print(f"Translated Response: {response}")
            # text_to_speech(response, language)


# Run the tutor
try:
    if __name__ == "__main__":
        asyncio.run(ai_tutor_voice())
except KeyboardInterrupt:
    print("Exiting program.")
    sys.exit(0)

