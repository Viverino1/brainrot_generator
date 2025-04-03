import os
import asyncio
import edge_tts

async def _generate(text, output_path):
  # Use a male voice with natural intonation
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate(text, output_path):
  # Ensure output directory exists
  os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
  
  # Run the async function
  asyncio.run(_generate(text, output_path))