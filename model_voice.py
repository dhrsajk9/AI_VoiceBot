from dotenv import load_dotenv
import os
from gtts import gTTS
import subprocess
import platform
from pydub import AudioSegment  # Needed to convert mp3 to wav
import elevenlabs
from elevenlabs.client import ElevenLabs

load_dotenv()

# Get ElevenLabs API key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# ===== gTTS Text-to-Speech (Old Style) =====
def gtts_text_to_speech_old(input_text, output_filepath):
    language = "en"
    audio_obj = gTTS(text=input_text, lang=language, slow=False)
    audio_obj.save(output_filepath)

# ===== ElevenLabs TTS (Old Style) =====
def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

# ===== gTTS with Playback =====
def gtts_text_to_speech(input_text, output_filepath):
    language = "en"
    audio_obj = gTTS(text=input_text, lang=language, slow=False)
    audio_obj.save(output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            # Convert to WAV before playback (SoundPlayer only supports WAV)
            wav_path = output_filepath.replace(".mp3", ".wav")
            AudioSegment.from_file(output_filepath).export(wav_path, format="wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])  # or use 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# ===== ElevenLabs with Playback (Final Autoplay-Safe Version) =====
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    temp_mp3 = "temp_output.mp3"
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, temp_mp3)

    # Convert to WAV for autoplay on Windows
    wav_path = output_filepath.replace(".mp3", ".wav")
    AudioSegment.from_file(temp_mp3).export(wav_path, format="wav")

    # Autoplay
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', temp_mp3])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', temp_mp3])
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Playback error: {e}")

    return temp_mp3  # Return for Gradio playback if needed

# ====== Example usage (Uncomment to test) ======
# input_text = "Hi, I am Dhrsaj. Testing ElevenLabs autoplay"
# text_to_speech_with_elevenlabs(input_text, output_filepath="final.mp3")
