import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import time
from pydub import AudioSegment
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationChain

# Set environment variable for ffmpeg 
os.environ["IMAGEIO_FFMPEG_EXE"] = "/path/to/ffmpeg"

# Set your OpenAI API key
openai_api_key = "sk-proj-8LWKh54dXcVosz8hbSlgT3BlbkFJf4zWnIBw0fhBK01E21XJ"

# Azure OpenAI configuration
api_version = "2023-12-01-preview"
endpoint = "https://gpt-course.openai.azure.com"
api_key = "72e0e504082a45f594cc2308b8d01ca9"
deployment_name = "gpt-4"

# Ensure directory exists
def ensure_dir(file_path):
    """
    Ensure directory exists.
    Input: file_path (str)
    Output: Creates directory if it does not exist
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)

# Function to download YouTube video and extract audio
def download_and_extract_audio(video_url, video_output_path, audio_output_path):
    """
    Download YouTube video and extract audio.
    Input: video_url (str), video_output_path (str), audio_output_path (str)
    Output: audio_output_path (str)
    """
    try:
        # Ensure directories exist
        ensure_dir(video_output_path)
        ensure_dir(os.path.dirname(audio_output_path))
        
        # Download the video
        yt = YouTube(video_url)
        video_path = yt.streams.get_highest_resolution().download(output_path=video_output_path)

        # Extract audio from video
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_output_path)
        
        return audio_output_path
    
    # Handle exceptions
    except Exception as e:
        print(f"Error downloading or processing video: {e}")
        return None

# Function to recognize speech from audio file with retries
def recognize_speech_with_retries(recognizer, audio_data, retries=3, delay=5):
    """
    Recognize speech from audio file with retries.
    Input: recognizer (SpeechRecognizer), audio_data (AudioData), retries (int), delay (int)
    Output: text (str)
    """
    for attempt in range(retries):
        try:
            return recognizer.recognize_google(audio_data)
        except sr.RequestError as e:
            print(f"Recognition request failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
    return None

# Function to split audio into chunks
def split_audio(audio_path, chunk_length_ms=60000):
    """
    Split audio into chunks.
    Input: audio_path (str), chunk_length_ms (int)
    Output: chunks (list)
    """
    audio = AudioSegment.from_wav(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

# Function to process each audio chunk
def process_audio_chunks(chunks):
    """
    Process each audio chunk.
    Input: chunks (list)
    Output: full_text (str)
    """
    # Initialize SpeechRecognizer
    recognizer = sr.Recognizer()
    full_text = ""
    
    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            chunk_text = recognize_speech_with_retries(recognizer, audio_data)
            if chunk_text:
                full_text += chunk_text + " "
    
    return full_text

# Function to summarize text using AzureChatOpenAI
def summarize_text(text, max_sentences=3):
    """
    Summarize text using AzureChatOpenAI.
    Input: text (str), max_sentences (int)
    Output: summary (str)
    """
    template = """System: Provide a helpful summary in {max_sentences} sentences.
    Human: {text}
    AI"""
    prompt = PromptTemplate.from_template(template)
    agent = AzureChatOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
        deployment_name=deployment_name
    )
    chain = LLMChain(
        llm=agent,
        prompt=prompt
    )
    summary = chain.run(reference="", text=text, max_sentences=max_sentences)
    return summary.strip()

# YouTube video URL
video_url = "https://www.youtube.com/watch?v=NIJ3vJKKDGk"

# Paths to save video and audio
video_output_path = "path_to_save_video"
audio_output_path = "path_to_save_audio/audio.wav"

# Download video and extract audio
audio_path = download_and_extract_audio(video_url, video_output_path, audio_output_path)

if audio_path:
    print("HEYYYYYY HOOOOOOMIEEEE1")
    
    # Split audio into chunks
    audio_chunks = split_audio(audio_path)
    
    print("HEYYYYYY HOOOOOOMIEEEE2")
    
    # Process each audio chunk
    text = process_audio_chunks(audio_chunks)

    if text:
        print("HEYYYYYY HOOOOOOMIEEEE3")
        print("Extracted Text:\n", text)

        # Summarize text using Langchain and AzureChatOpenAI
        summary_text = summarize_text(text, max_sentences=3)
        print("Summary:\n", summary_text)
    else:
        print("Speech recognition failed.")
else:
    print("Invalid URL. Please enter a valid YouTube URL.")
