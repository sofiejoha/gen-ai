from transformers import Blip2Processor, Blip2ForConditionalGeneration, BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from moviepy.editor import VideoFileClip
import random
import numpy as np
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from config import *
from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def load_model_and_processor(model_choice):
    """
    Load the chosen model and processor.
    Input: model_choice (str)
    Output: processor, model
    """
    # Load the chosen model and processor
    if model_choice == "BLIP-2":
        processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
    elif model_choice == "BLIP":
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    else:
        raise ValueError("Invalid model choice. Please choose 'BLIP' or 'BLIP-2'.")
    
    model.to(device)
    return processor, model


def extract_frames(video_path, num_frames=10):
    """
    Extract frames from a video using scene detection. 
    Input: video_path (str), num_frames (int)
    Output: frames (list of PIL.Image)
    """
    # Open the video and create a scene manager
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    # Perform scene detection
    scene_manager.detect_scenes(video)

    # Get the list of scenes, each scene is a tuple (start_frame, end_frame)
    scene_list = scene_manager.get_scene_list()

    # Select frames from detected scenes
    video_clip = VideoFileClip(video_path)
    frames = []

    for scene in scene_list:
        # Get the middle frame of the scene
        start_frame, end_frame = scene[0].get_frames(), scene[1].get_frames()
        mid_frame_time = (start_frame + end_frame) // 2 / video_clip.fps
        # Extract the frame
        frame = video_clip.get_frame(mid_frame_time)
        # Convert the frame to PIL Image
        image = Image.fromarray(np.uint8(frame)).convert("RGB")
        # Append the image to the list of frames
        frames.append(image)
        # Break if we have enough frames
        if len(frames) >= num_frames:
            break

    return frames

def generate_caption(image, processor, model):
    """
    Generate caption for an image.
    Input: image (PIL.Image), processor, model
    Output: caption (str)
    """
    # Process the image
    inputs = processor(images = image, return_tensors = "pt").to(device)
    # Generate caption using the model
    out = model.generate(**inputs)
    # Decode the caption
    caption = processor.decode(out[0], skip_special_tokens = True)
    return caption

def summarize_image_captions(captions, max_sentences = 5):
    """
    Generate a summary of image captions using LangChain and GPT-4.
    Input: captions (list of str), max_sentences (int)
    Output: summary (str)
    """
    text = " ".join(captions)
    template = """System: Provide a helpful summary in {max_sentences} sentences.
    Human: {text}
    AI"""
    prompt = PromptTemplate.from_template(template)
    agent = AzureChatOpenAI(
        api_version = API_VERSION,
        azure_endpoint = ENDPOINT,
        api_key = API_KEY,
        deployment_name = DEPLOYMENT_NAME
    )
    chain = LLMChain(
        llm = agent,
        prompt = prompt
    )
    summary = chain.run(reference = "", text = text, max_sentences = max_sentences)
    return summary.strip()

