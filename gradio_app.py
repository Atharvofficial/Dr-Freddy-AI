import gradio as gr
import os
from brain_setup import encode_image, analyse_image_with_query
from user_voice import transcribe_with_groq
from doctor_voice import text_to_speech_with_elevenlabs
from fastapi import FastAPI
import uvicorn


system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose.Your name will be Dr Freddy. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please and if someone asks you a general question other than medical related questions please handle them gracefully as if a real doctor would do"""



def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    if image_filepath:
        doctor_response = analyse_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor



# CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* --- General App Styling --- */
body {
    background-color: #f0f4f8; /* Light blue-gray background */
    font-family: 'Inter', sans-serif;
}
.gradio-container {
    background-color: #ffffff;
    border-radius: 20px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    max-width: 900px;
    margin: 2rem auto; /* Center the app */
}

/* --- Title --- */
h1 {
    color: #1a3a5d; /* Dark professional blue */
    text-align: center;
    font-size: 2.5em !important;
    font-weight: 700;
    margin-bottom: 2rem !important;
    letter-spacing: -1px;
}

/* --- Component Labels --- */
.gr-panel .gr-label > span, .gr-box .gr-label > span {
    font-weight: 600 !important;
    color: #4a5568; /* Gray text */
    font-size: 1.1em !important;
    margin-bottom: 0.5rem;
}

/* --- Input/Output Component Containers --- */
.gr-box, .gr-panel {
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    box-shadow: none !important;
    background-color: #f7fafc !important; /* Very light gray */
    padding: 1.5rem !important;
}

/* --- Style the textboxes --- */
textarea {
    border: 1px solid #cbd5e0 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    padding: 0.75rem !important;
    font-size: 1em !important;
    transition: all 0.2s ease-in-out;
    min-height: 180px; /* Increased height */
}
textarea:focus {
    border-color: #4299e1 !important;
    box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.5) !important;
    outline: none;
}

/* --- Buttons --- */
.gr-button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    border: none !important;
}

/* Primary Button (Submit) */
.gr-button-primary {
    background: #2563eb !important; /* Vibrant blue */
    color: white !important;
}
.gr-button-primary:hover {
    background: #1d4ed8 !important; /* Darker blue on hover */
    transform: translateY(-2px);
    box-shadow: 0 7px 10px -3px rgba(37, 99, 235, 0.3), 0 4px 6px -2px rgba(37, 99, 235, 0.2) !important;
}
.gr-button-primary:active {
    transform: translateY(0);
}

/* Secondary Buttons (Clear, Flag) */
.gr-button-secondary {
    background: #e2e8f0 !important; /* Light gray */
    color: #4a5568 !important;
}
.gr-button-secondary:hover {
    background: #cbd5e0 !important; /* Darker gray */
    transform: translateY(-2px);
}
"""


# INTERFACE
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Dr Freddy's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="DR FREDDY AI",
    css=custom_css,
    allow_flagging="never"
)

# VERCEL DEPLOYMENT
# CREATE A FASTAPI APP
app = FastAPI()

# MOUNT THE GRADIO APP ONTO THE FASTAPI APP
app = gr.mount_gradio_app(app, iface, path="/")
