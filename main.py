from S_to_T import *
from captions import *
from overall import *

def main(video_url, model_choice, progress_callback=None):
   
    # Function for updating the progress bar 
    def update_progress(step, message):
        if progress_callback:
            progress_callback(step, message)
            
    update_progress(10, "Loading model and processor...") # Initial progress bar 
    
    # Load the chosen model and processor
    processor, model = load_model_and_processor(model_choice)
    update_progress(20, "Downloading and extracting audio...")
    video_output_path = "path_to_save_video"
    audio_output_path = "path_to_save_audio/audio.wav"

    audio_path, video_path = download_and_extract_audio(video_url, video_output_path, audio_output_path)
    update_progress(30, "Audio and video downloaded successfully...")
    if audio_path and video_path:
        print("Audio and video downloaded successfully.")
        
        # Process audio for speech-to-text
        audio_chunks = split_audio(audio_path)
        update_progress(40, "Processing audio...")
        text = process_audio_chunks(audio_chunks)

        if text:
            print("Extracted Text:\n", text)
            summary_text = summarize_text(text, max_sentences=3)
            update_progress(50, "Summarizing audio...")
            print("Text Summary:\n", summary_text)
        else:
            print("Speech recognition failed.")
            return
        
        # Process video for image captioning
        print("Processing video for image captioning...")
        frames = extract_frames(video_path)
        update_progress(70, "Extracting frames from video...")
        print(f"Extracted {len(frames)} frames from the video.")
        captions = [generate_caption(frame, processor, model) for frame in frames]
        print("Generated captions for all frames.")
        summary_captions = summarize_image_captions(captions, max_sentences=3)
        print("Image Captions Summary:\n", summary_captions)
        update_progress(90, "Summarizing...")

        # Generate overall summary
        overall_summary = summarize_overall(summary_text, summary_captions, personality = 'professor', max_sentences = 5)
        print("Overall Summary:\n", overall_summary)
        return overall_summary

    else:
        print("Failed to download video or extract audio.")

if __name__ == "__main__":
    main()