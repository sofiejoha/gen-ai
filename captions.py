from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import torch
from moviepy.editor import VideoFileClip
import random
import numpy as np
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the processor and model
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")

# Move model to GPU
model.to(device)

def extract_frames(video_path, num_frames=50):
    """
    Extract frames from video.
    Input: video_path (str), num_frames (int)
    Output: frames (list of PIL.Image)
    """
    video_clip = VideoFileClip(video_path)
    total_frames = int(video_clip.fps * video_clip.duration)
    frame_times = sorted(random.sample(range(total_frames), num_frames))
    frames = []

    for t in frame_times:
        frame = video_clip.get_frame(t / video_clip.fps)
        image = Image.fromarray(np.uint8(frame)).convert("RGB")
        frames.append(image)

    return frames

def generate_caption(image):
    """
    Generate caption for an image.
    Input: image (PIL.Image)
    Output: caption (str)
    """
    # Process the image
    inputs = processor(images=image, return_tensors="pt").to(device)
    # Generate caption using the model
    out = model.generate(**inputs)
    # Decode the caption
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# Extract frames from a video and generate captions for each frame
video_path = "path_to_save_video/How To Eat Like A Pro Cyclist.mp4"
frames = extract_frames(video_path)
captions = [generate_caption(frame) for frame in frames]

# Print the generated captions
for i, caption in enumerate(captions):
    print(f"Caption {i + 1}: {caption}")

# Azure OpenAI configuration
api_version = "2023-12-01-preview"
endpoint = "https://gpt-course.openai.azure.com"
api_key = "72e0e504082a45f594cc2308b8d01ca9"
deployment_name = "gpt-4"

# Function to summarize image captions using LangChain and GPT-4
def summarize_image_captions(captions, max_sentences=5):
    """
    Summarize image captions using LangChain and GPT-4.
    Input: captions (list of str), max_sentences (int)
    Output: summary (str)
    """
    text = " ".join(captions)
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

# Summarize the captions
summary_captions = summarize_image_captions(captions, max_sentences=5)
print("Image Captions Summary:\n", summary_captions)



"""
py -c "import sys; from subprocess import run; packages = ['transformers', 'torch', 'Pillow', 'moviepy', 'numpy', 'langchain']; run([sys.executable, '-m', 'pip', 'install'] + packages)"
"""