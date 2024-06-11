# This file was used for testing the BLIP models and for methods to extract frames. 
# It is not used in the main product. 

import numpy as np
import cv2
import torch
from PIL import Image
import os
from io import BytesIO
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai
from transformers import BlipProcessor, Blip2Processor, AutoProcessor, BlipForConditionalGeneration, Blip2ForConditionalGeneration


# Set OpenAI API key
openai_api_key = "sk-proj-8LWKh54dXcVosz8hbSlgT3BlbkFJf4zWnIBw0fhBK01E21XJ"

# Azure OpenAI configuration
api_version = "2023-12-01-preview"
endpoint = "https://gpt-course.openai.azure.com"
api_key = "72e0e504082a45f594cc2308b8d01ca9"
deployment_name = "gpt-4"

def extract_frames(video_path, interval = 5):
    """
    Function to extract frames from the video at specified intervals.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []

    # Getting the frame rate (frames per second)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # Loop to read frames from the video capture object
    while cap.isOpened():
        # Get the current frame ID (position of the video file)
        frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        ret, frame = cap.read()

        # If no frame is returned, it is the end of the video
        if not ret:
            break
        if frame_id % (interval * frame_rate) == 0:
            frames.append(frame)
    cap.release()

    return frames 


def detect_scenes(video_path):
    """
    Function to identify significant changes in the video content.
    By detecting scene changes, we can select keyframes from the video that are
    the most likely to be representative of different segments of the contents. 
    """
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    scenes = []

    # Loop to read frames from the video capture object
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if prev_frame is not None:
            # Calculate the absolute difference between current frame and previous frame 
            diff = cv2.absdiff(frame, prev_frame)

            # Convert the difference frame to grayscale 
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            # Count the number of non-zero pixels in the grayscale difference frame
            non_zero_count = cv2.countNonZero(gray_diff)
            
            # If the number of 
            if non_zero_count > 450000:
                scenes.append(frame)

        prev_frame = frame
    cap.release()
    return scenes


def summarize_img(frames, max_sentences = 3):
    """
    Summarize images using AzureChatOpenAI
    """
    
    # Define the prompt template 
    template = """System: Provide a helpful summary in {max_sentences} sentences.
    Human: {text}
    AI"""
    prompt = PromptTemplate.from_template(template)

    # Initialize AzureChatOpenAI agent 
    agent = AzureChatOpenAI(
        api_version = api_version,
        azure_endpoint = endpoint,
        api_key = api_key,
        deployment_name = deployment_name
    )

    chain = LLMChain(
        llm = agent,
        prompt = prompt
    )

    captions = []
    for frame in frames:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Convert the PIL image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Craft the prompt
        prompt_text = 'This is an image from a video. Describe it in a few sentences. If you do not know the answer, it is very important that you do not lie!'
        
        caption = chain.run(reference = img_byte_arr, text = prompt_text, max_sentences = max_sentences)
        captions.append(caption)

    return captions



def blip_caption_images(frames):
    """
    Function to use the BLIP model for image captioning. It uses a vision encoder and
    a text decoder. 
    """
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b").to("cuda" if torch.cuda.is_available() else "cpu")
    
    captions = []
    for frame in frames:
        # Process the image and generate a caption 
        inputs = processor(images = Image.fromarray(frame), return_tensors = 'pt').to('cuda' if torch.cuda.is_available() else 'cpu')
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens = True)
        captions.append(caption)

    return captions



# Test the function
if __name__ == "__main__":
    # Testing with a random video
    video_path = 'test_video.mp4'  
    output_dir = 'extracted_frames'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok = True)

    # Extract frames
    frames = extract_frames(video_path, interval = 20)
    
    # Captions using OpenAI's GPT-4
    captions = summarize_img(frames)

    # Captions using BLIP 
    blip_captions = blip_caption_images(frames)

    for i, (frame, caption) in enumerate(zip(frames, captions)):
        frame_path = os.path.join(output_dir, f'frame_{i}.jpg')
        cv2.imwrite(frame_path, frame)
        print(f'Caption for frame {i}: {caption}')

    print(f'Extracted {len(frames)} frames and saved to {output_dir}')

