import os
import json
import requests
import subprocess
import time

def generate(audio_path, text, output_path):
    print("Starting subtitle generation...")
    
    # Start Gentle web service
    gentle_path = "/Applications/Gentle.app/Contents/MacOS/gentle"
    server_process = subprocess.Popen([gentle_path, "--serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Starting Gentle server...")
    time.sleep(5)  # Give the server some time to start
    
    try:
        # Use Gentle's web API with correct endpoint
        url = "http://localhost:8765/transcriptions?async=false"
        print("Sending request to Gentle server...")
        
        with open(audio_path, 'rb') as audio_file:
            files = {
                'audio': ('audio.wav', audio_file, 'audio/wav'),
                'transcript': ('transcript.txt', text, 'text/plain')
            }
            response = requests.post(url, files=files)
        
        if response.status_code != 200:
            raise Exception(f"Gentle alignment failed with status code {response.status_code}")
        
        alignment = response.json()
        
        # Generate SRT format
        srt_lines = []
        counter = 1
        
        for word in alignment['words']:
            if 'start' not in word or 'end' not in word:
                continue
                
            start_time = format_timestamp(word['start'])
            end_time = format_timestamp(word['end'])
            
            srt_lines.append(str(counter))
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(word['word'])
            srt_lines.append("")
            
            counter += 1
        
        # Write the SRT file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_lines))
        
        print("Subtitle generation completed!")
        
    finally:
        # Clean up: terminate the server
        server_process.terminate()
        server_process.wait()

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
  