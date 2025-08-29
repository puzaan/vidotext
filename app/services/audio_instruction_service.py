from openai import OpenAI
import base64
import json
import os
from app.core.config import settings

def get_openai_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_audio_descriptions(frame_paths):
    """
    Generate descriptions focused only on exercise instructions (not detailed analysis)
    """
    client = get_openai_client()
    descriptions = []
    
    for image_path in frame_paths:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = """
        Look at this exercise frame and describe ONLY what instructions should be given:
        
        1. What movement is happening RIGHT NOW
        2. What should the person be doing at this moment
        3. Key form cues for this specific position
        4. Breathing instruction for this phase
        
        Be concise and focus only on actionable instructions. No analysis, no benefits, no muscle names.
        Example: "Bend your knees and lower your hips" instead of "This is a squat targeting quadriceps"
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=150,  # Shorter for instructions only
            temperature=0.1,
        )
        
        descriptions.append(response.choices[0].message.content)
    
    return descriptions

def generate_audio_instructions(descriptions, video_duration):
    """
    Combine frame descriptions into timed exercise instructions
    """
    client = get_openai_client()
    
    prompt = f"""
    You are a fitness instructor creating real-time audio guidance. 
    Combine these frame descriptions into continuous exercise instructions that will last exactly {video_duration} seconds.
    
    FRAME DESCRIPTIONS:
    {json.dumps(descriptions, indent=2)}
    
    Create instructions that:
    1. Flow naturally from one movement to the next
    2. Are exactly {video_duration} seconds long when spoken
    3. Use clear, actionable language
    4. Include breathing cues (breathe in/out)
    5. Match the pace and timing of the exercise
    6. No introductions or conclusions - just the exercise guidance
    
    Speak as if you're guiding someone through the exercise in real-time.
    Use imperative language: "Bend your knees", "Keep your back straight", etc.
    
    Calculate the word count for {video_duration} seconds (approx 2-2.5 words per second).
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "You are a fitness instructor creating perfectly timed exercise audio guidance. You create concise, actionable instructions that match video duration exactly."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        max_tokens=600,
        temperature=0.1,
    )
    
    return response.choices[0].message.content

def analyze_video_for_audio(video_path):
    """
    Analyze video specifically for audio instruction generation
    """
    # Extract keyframes
    from app.services.video_processor import extract_keyframes
    frame_paths = extract_keyframes(video_path, max_frames=12)
    
    if not frame_paths or len(frame_paths) < 3:
        raise ValueError("Could not extract enough frames from video")
    
    # Generate exercise instructions (not analysis)
    audio_descriptions = generate_audio_descriptions(frame_paths)
    
    # Get video duration
    video_duration = get_video_duration(video_path)
    
    # Generate final audio instructions
    instructions_text = generate_audio_instructions(audio_descriptions, video_duration)
    
    # Clean up frame files
    for path in frame_paths:
        if os.path.exists(path):
            os.remove(path)
    
    return instructions_text, video_duration

def get_video_duration(video_path):
    """
    Extract video duration using OpenCV
    """
    import cv2
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    cap.release()
    return duration