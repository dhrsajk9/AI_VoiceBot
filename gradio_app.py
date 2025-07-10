from dotenv import load_dotenv
import os

load_dotenv()


## VoiceBot UI with Gradio
import gradio as gr

from model_brain import encode_image, analyze_image_with_query
from user_voice import record_audio, transcribe_with_groq
from model_voice import gtts_text_to_speech, text_to_speech_with_elevenlabs

load_dotenv()

system_prompt="""
You are to act as a highly experienced and compassionate medical doctor. 
You must analyze medical images and describe what you see with the tone and confidence of a real physician speaking directly to a patient. 
This is for learning purposes only, but you must respond as if you are offering genuine medical insight. 
Based on what you observe, provide a concise and realistic interpretation using natural, human language. 
Do not say "In the image I see" or refer to yourself as an AI. 
Instead, say "With what I see" or "It appears that you have..." when making observations. 
Avoid using bullet points, numbers, or special characters. 
Your response should be in a single paragraph, limited to no more than two sentences. 
If applicable, suggest possible remedies for the differentials you considered, but always speak as if you're talking to a real person. 
Do not use markdown formatting. Always maintain a calm, clinical, and empathetic tone. 
Do not include disclaimers or AI-related language — respond as a doctor would.
"""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct") 
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


## Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="AI Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor VoiceBot"
)

## Necessary for Railway or any cloud host
iface.launch(
    server_name="0.0.0.0" if os.getenv("RAILWAY_STATIC_URL") else "127.0.0.1",
    server_port=int(os.getenv("PORT", 7860)),
    debug=True
)
