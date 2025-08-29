from gtts import gTTS
from pydub import AudioSegment
import os
from app.core.config import settings
from app.services.audio_instruction_service import analyze_video_for_audio

def generate_instruction_audio(video_path):
    """
    Complete audio generation process from video to final audio
    """
    # Create audio directory if it doesn't exist
    if not os.path.exists(settings.AUDIO_DIR):
        os.makedirs(settings.AUDIO_DIR)
    
    # Analyze video and generate instructions
    instructions_text, video_duration = analyze_video_for_audio(video_path)
    
    # Create filename based on video name
    video_name = os.path.basename(video_path).split('.')[0]
    audio_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_instructions.mp3")
    
    # Save instructions text for reference
    text_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_instructions.txt")
    with open(text_filename, "w") as f:
        f.write(instructions_text)
    
    # Generate audio with precise duration matching
    audio_filename = create_precise_audio(instructions_text, video_duration, audio_filename)
    
    # Verify duration
    audio = AudioSegment.from_mp3(audio_filename)
    final_duration = len(audio) / 1000
    
    return audio_filename, final_duration, instructions_text

def create_precise_audio(text, target_duration, output_filename):
    """
    Create audio that exactly matches the target duration
    """
    # First pass: generate initial audio
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_filename)
    
    # Check duration and adjust if needed
    audio = AudioSegment.from_mp3(output_filename)
    current_duration = len(audio) / 1000
    
    if abs(current_duration - target_duration) > 1.0:  # If more than 1 second difference
        # Adjust speech rate to match target duration
        speed_factor = current_duration / target_duration
        adjusted_audio = audio.speedup(playback_speed=speed_factor)
        adjusted_audio.export(output_filename, format="mp3")
    
    return output_filename