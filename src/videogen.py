import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip

def generate(audio_path, output_path):
    print("Starting video generation...")
    
    # Get random video from assets
    footage_dir = "/Users/vivekmaddineni/Documents/Brainrot_Generator/assets/brainrot-footage"
    video_files = [f for f in os.listdir(footage_dir) if f.endswith(('.mp4', '.mov'))]
    
    if not video_files:
        raise Exception("No video files found in brainrot-footage directory")
    
    random_video = random.choice(video_files)
    video_path = os.path.join(footage_dir, random_video)
    print(f"Selected video: {random_video}")
    
    try:
        # Load the audio to get its duration
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        print(f"Audio duration: {audio_duration:.2f} seconds")
        
        # Load and process video
        video = VideoFileClip(video_path)
        print(f"Video duration: {video.duration:.2f} seconds")
        
        if video.duration < audio_duration:
            raise Exception("Video is shorter than audio")
        
        # Pick a random start point that allows for audio_duration
        max_start = video.duration - audio_duration
        start_time = random.uniform(0, max_start)
        print(f"Cutting video from {start_time:.2f} to {start_time + audio_duration:.2f}")
        
        # Cut the video to match audio duration
        trimmed_video = video.subclip(start_time, start_time + audio_duration)
        
        # Crop video to vertical format (9:16 aspect ratio)
        w, h = trimmed_video.size
        target_w = int(h * 9/16)  # Calculate width for 9:16 ratio
        x_center = w/2
        crop_x1 = int(x_center - target_w/2)
        crop_x2 = int(x_center + target_w/2)
        trimmed_video = trimmed_video.crop(x1=crop_x1, x2=crop_x2)
        
        # Combine video with audio
        final_video = trimmed_video.set_audio(audio)
        
        # Write the final video
        print("Rendering final video...")
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='medium'
        )
        
        # Clean up
        audio.close()
        video.close()
        trimmed_video.close()
        final_video.close()
        
        print("Video generation completed!")
        
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        raise