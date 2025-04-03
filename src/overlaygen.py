import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

def generate(video_path, srt_path, output_path):
    print("Adding subtitles to video...")
    
    # Load the video
    video = VideoFileClip(video_path)
    
    # Load subtitles
    subs = pysrt.open(srt_path)
    
    # Convert srt times to seconds
    subtitle_clips = []
    
    # Configure text style
    fontsize = int(video.h * 0.07)  # Responsive font size based on video height
    
    for sub in subs:
        start_time = sub.start.seconds + (sub.start.milliseconds / 1000)
        end_time = sub.end.seconds + (sub.end.milliseconds / 1000)
        duration = end_time - start_time
        
        # Create shadow layer
        shadow = (TextClip(sub.text.upper(), 
                          fontsize=fontsize,
                          color='black',
                          font='Arial-Black',
                          stroke_color='black',
                          stroke_width=4)
                 .set_position(('center', 'center'))
                 .set_duration(duration)
                 .set_start(start_time)
                 .margin(opacity=0.8))  # Add blur effect to shadow
        
        # Create main text layer
        txt_clip = (TextClip(sub.text.upper(), 
                            fontsize=fontsize,
                            color='white',
                            font='Arial-Black',
                            stroke_color='black',
                            stroke_width=2)
                   .set_position(('center', 'center'))
                   .set_duration(duration)
                   .set_start(start_time))
        
        subtitle_clips.extend([shadow, txt_clip])
    
    # Combine video with subtitles
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    # Write the final video
    print("Rendering video with subtitles...")
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        threads=4,
        preset='medium'
    )
    
    # Clean up
    video.close()
    final_video.close()
    
    print("Subtitles overlay completed!")