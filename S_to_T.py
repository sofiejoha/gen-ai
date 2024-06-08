import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import time
from pydub import AudioSegment
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from captions import extract_frames, generate_caption, summarize_image_captions

# Set environment variable for ffmpeg 
os.environ["IMAGEIO_FFMPEG_EXE"] = "/path/to/ffmpeg"

# Set your OpenAI API key
openai_api_key = "sk-proj-8LWKh54dXcVosz8hbSlgT3BlbkFJf4zWnIBw0fhBK01E21XJ"

# Azure OpenAI configuration
api_version = "2023-12-01-preview"
endpoint = "https://gpt-course.openai.azure.com"
api_key = "72e0e504082a45f594cc2308b8d01ca9"
deployment_name = "gpt-4"

def ensure_dir(file_path):
    """
    Ensure that the directory for the given file path exists.
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def download_and_extract_audio(video_url, video_output_path, audio_output_path):
    """
    Download a YouTube video and extract the audio.
    Input: video_url (str), video_output_path (str), audio_output_path (str)
    Output: audio_output_path (str), video_path (str)
    """
    try:
        ensure_dir(video_output_path)
        ensure_dir(os.path.dirname(audio_output_path))
        
        yt = YouTube(video_url)
        video_path = yt.streams.get_highest_resolution().download(output_path=video_output_path)

        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_output_path)
        
        return audio_output_path, video_path
    except Exception as e:
        print(f"Error downloading or processing video: {e}")
        return None, None

def recognize_speech_with_retries(recognizer, audio_data, retries=3, delay=5):
    """
    Recognize speech from audio data with retries.
    Input: recognizer (SpeechRecognizer), audio_data, retries (int), delay (int)
    Output: text (str)
    """
    # Retry speech recognition if it fails
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

def split_audio(audio_path, chunk_length_ms=60000):
    """
    Split an audio file into chunks of a specified length.
    Input: audio_path (str), chunk_length_ms (int)
    Output: chunks (list of AudioSegment)
    """
    audio = AudioSegment.from_wav(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def process_audio_chunks(chunks):
    """
    Process audio chunks for speech recognition.
    Input: chunks (list of AudioSegment)
    Output: full_text (str)
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    full_text = ""

    # Process each chunk for speech recognition
    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        
        # Recognize speech from the chunk
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            chunk_text = recognize_speech_with_retries(recognizer, audio_data)
            if chunk_text:
                full_text += chunk_text + " "
    
    return full_text

def summarize_text(text, max_sentences=3):
    """
    Summarize text using LangChain and GPT-4.
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