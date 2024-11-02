# Audio/Video Transcription and Summarization Application

## Overview

This application provides a comprehensive solution for processing audio and video files by extracting audio, transcribing it into text, and generating concise summaries of the transcriptions. Utilizing the advanced Whisper model for transcription and the Groq API for summarization, this tool aims to streamline the analysis of multimedia content.

## Features

- **Audio Extraction**: The app can automatically extract audio from various video formats, allowing for seamless processing without manual intervention.
- **Transcription**: Using OpenAI's Whisper model, the app accurately converts audio content into text, making it accessible for further analysis.
- **Summarization**: Leveraging the Groq API, the app generates clear and concise summaries of the transcribed text, facilitating quick understanding of the content.
- **User-Friendly Interface**: The application is designed to be straightforward, enabling users to upload files and receive outputs with minimal effort.
- **Supports Multiple Formats**: Accepts a wide range of audio and video file formats for flexibility in usage.

## Installation

To use this application, you'll need to install the necessary libraries. You can run the following commands in your Python environment:

```bash
!pip install -q git+https://github.com/openai/whisper.git
!pip install -q groq ffmpeg-python
```

## Usage

1. **Upload Audio or Video Files**: Users can upload their audio or video files directly into the application.
2. **Processing**: The application will automatically:
   - Extract audio from video files (if applicable).
   - Transcribe the audio to text using the Whisper model.
   - Summarize the transcription using the Groq API.
3. **Output**: The transcription and summary are displayed to the user for easy reference.

## How It Works

- **Audio Extraction**: The application uses the `ffmpeg` library to extract audio from video files, saving it as a temporary audio file.
- **Transcription**: The Whisper model is utilized to convert the extracted audio (or uploaded audio files) into text.
- **Summarization**: The transcribed text is sent to the Groq API, which generates a summary of the content, providing a concise overview of the information conveyed in the audio.

## Requirements

- Python 3.x
- Access to the Groq API (API key needed)

## Contributions

Contributions to enhance the functionality of this application are welcome! Feel free to fork the repository and submit a pull request with your improvements.
