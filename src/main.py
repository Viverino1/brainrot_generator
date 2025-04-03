import os
import overlaygen
import storygen
import speechgen
import srtgen
import videogen

project_dir = "/Users/vivekmaddineni/Documents/Brainrot_Generator"
speech_path = os.path.join(project_dir, "temp/speech.wav")
srt_path = os.path.join(project_dir, "temp/subtitles.srt")
video_no_sub_path = os.path.join(project_dir, "temp/video_no_sub.mp4")
video_with_sub_path = os.path.join(project_dir, "temp/video_with_sub.mp4")

title, script = storygen.generate()
story = title + "\n\n" + script
speechgen.generate(story, speech_path)
srtgen.generate(speech_path, story, srt_path)
videogen.generate(speech_path, video_no_sub_path)
overlaygen.generate(video_no_sub_path, srt_path, video_with_sub_path)