#deploy directly in huggingface..

# __requirements.txt__
# git+https://github.com/openai/whisper.git
# moviepy
# transformers
# gradio


import whisper
from moviepy.editor import VideoFileClip
from transformers import BartForConditionalGeneration, BartTokenizer
import gradio as gr
import os

# Load models
whisper_model = whisper.load_model("base")
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
summarizer_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def transcribe_and_summarize(video_file):
    try:
        # Step 1: Process the video
        clip = VideoFileClip(video_file)
        audio_file = "audio.wav"
        clip.audio.write_audiofile(audio_file)

        # Step 2: Transcribe audio
        result = whisper_model.transcribe(audio_file)
        transcribed_text = result['text']

        # Step 3: Summarize text
        inputs = tokenizer(transcribed_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarizer_model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Clean up the audio file
        os.remove(audio_file)

        return transcribed_text, summary

    except Exception as e:
        return str(e), "Error occurred during processing."

# Create Gradio interface
iface = gr.Interface(
    fn=transcribe_and_summarize,
    inputs=gr.Video(label="Upload Video"),
    outputs=[
        gr.Textbox(label="Transcribed Text", lines=10),
        gr.Textbox(label="Summary", lines=5)
    ],
    title="Video Transcription and Summarization",
    description="Upload a video file to transcribe its audio and generate a summary of the transcribed text."
)

# Launch the interface
iface.launch()
