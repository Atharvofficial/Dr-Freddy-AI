#elevenlabs
#TEXT TO SPEECH USING ELEVENLABS
import os
import elevenlabs
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from elevenlabs import save
from elevenlabs.play import play

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def text_to_speech_with_elevenlabs(input_text,output_filepath):
  audio = elevenlabs.text_to_speech.convert(
    text=input_text,
    voice_id="onwK4e9ZLuTAKqWW03F9",
    model_id="eleven_turbo_v2",
    output_format="mp3_44100_128",
)
  # COLLECT ALL CHUNKS INTO A SINGLE BYTE OBJECT
  audio_bytes = b"".join(audio)
    
  # PLAY THE AUDIO
  play(audio_bytes)
    
  # SAVE THE AUDIO
  save(audio_bytes, output_filepath)
  

