



import os
import ffmpeg
import whisper
import streamlit as st
from groq import Groq

# Custom CSS for styling
st.markdown("""
    <style>
    /* Background gradient and color settings */
    .stApp {
        background-image: linear-gradient(to right, #2e2e2e, #454545);
        color: white;
        font-family: Arial, sans-serif;
    }
    /* Container box styling */
    .container {
        background-color: #333;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
    }
    /* Header styling */
    .header {
        color: #ffdd40;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
    }
    /* Subheader styling */
    .subheader {
        color: #f0f0f0;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    /* Button styling */
    .stButton>button {
        background-color: #ffdd40;
        color: #333;
        border-radius: 5px;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ffcc00;
        color: #222;
    }
    /* Footer styling */
    .footer {
        text-align: center;
        color: #cfcfcf;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description with styling
st.markdown("<div class='header'>🎙️ Audio/Video Transcription & Summarization</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Upload an audio or video file to get a transcription and a concise summary.</div>", unsafe_allow_html=True)

# Sidebar for settings and instructions
with st.sidebar:
    st.header("Settings")
    st.write("Customize your preferences:")
    enable_summary = st.checkbox("Enable Summarization", value=True)
    st.info("Note: Summarization uses the Groq API.")

# Retrieve the API key from environment variables or Streamlit secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Create a temporary directory
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

# Enhanced file upload area
st.markdown("<div class='container'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    label="Select an audio or video file",
    type=["mp4", "mov", "avi", "mkv", "wav", "mp3"],
    help="Supported formats: mp4, mov, avi, mkv, wav, mp3"
)

# Function to extract audio from video
def extract_audio(video_path, audio_path="temp/temp_audio.wav"):
    try:
        ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        st.error("Error processing file with FFmpeg: " + e.stderr.decode())
    return audio_path

# Function to transcribe audio using Whisper model
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Function to summarize text using Groq API
def summarize_text(text):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Summarize the following text: {text}"}],
        model="llama3-8b-8192"
    )
    summary = response.choices[0].message.content
    return summary

# Main processing function with progress indicators
def process_media(media_file):
    temp_file_path = os.path.join(temp_dir, media_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(media_file.getbuffer())

    # Extract audio if the file is a video
    if media_file.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        st.info("Extracting audio from video...")
        audio_path = extract_audio(temp_file_path)
    else:
        audio_path = temp_file_path

    # Transcribe audio
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(audio_path)
    st.success("Transcription completed!")
    st.write("### Transcription:")
    st.write(transcription)
    
    # Summarize transcription if enabled
    if enable_summary:
        with st.spinner("Generating summary..."):
            summary = summarize_text(transcription)
        st.success("Summary generated!")
        st.write("### Summary:")
        st.write(summary)

    # Cleanup
    os.remove(temp_file_path)
    if media_file.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        os.remove(audio_path)

if uploaded_file:
    st.info("Processing your file, please wait...")
    process_media(uploaded_file)
else:
    st.warning("Please upload an audio or video file to begin.")

# Footer with branding
st.markdown("""
    <div class="footer">
        &copy; 2024 TranscribePro. Developed by Abdullah Zunorain.
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
