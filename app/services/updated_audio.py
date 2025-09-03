
# from openai import OpenAI
# import base64
# import json
# import os
# import cv2
# from app.core.config import settings
# from app.services.video_processor import extract_keyframes

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# # ------------------------------------------------------
# # 1. Frame-level instruction extraction for beginners
# # ------------------------------------------------------
# def generate_frame_instructions(frame_paths):
#     """
#     Generate beginner-friendly, actionable cues for each frame
#     """
#     instructions = []

#     for image_path in frame_paths:
#         with open(image_path, "rb") as image_file:
#             base64_image = base64.b64encode(image_file.read()).decode("utf-8")

#         prompt = """
#         Analyze this exercise frame and provide clear, beginner-friendly instructions.
        
#         Focus on:
#         1. What body position should be achieved in this frame
#         2. Key form points for proper technique
#         3. Breathing guidance for this phase
#         4. Simple, direct instructions
        
#         Example: "Lower into position, keeping your chest up and knees behind toes. Inhale as you descend."
#         """

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {"type": "image_url",
#                          "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
#                          }
#                     ],
#                 }
#             ],
#             max_tokens=120,
#             temperature=0.2,
#         )

#         instructions.append(response.choices[0].message.content.strip())

#     return instructions


# # ------------------------------------------------------
# # 2. Create step-by-step exercise guide
# # ------------------------------------------------------
# def generate_coaching_script(frame_instructions):
#     """
#     Create a step-by-step guide to the exercise
#     """
#     prompt = f"""
#     Create a step-by-step guide for this exercise based on these frame instructions:
    
#     {json.dumps(frame_instructions, indent=2)}
    
#     Structure your guide as follows:
#     1. Explain the starting position in detail
#     2. Break down the movement phase by phase
#     3. Include breathing cues throughout
#     4. End with how to properly finish the exercise
    
#     Speak directly to the listener with clear, actionable instructions.
#     Use simple language and focus only on what to do, not why.
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system",
#              "content": "You are a fitness trainer giving direct exercise instructions."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=800,
#         temperature=0.3,
#     )

#     return response.choices[0].message.content.strip()


# # ------------------------------------------------------
# # 3. Convert script into clear audio
# # ------------------------------------------------------
# def generate_instruction_audio(script_text, video_path):
#     """
#     Convert coaching script into clear audio instructions
#     """
#     # Create audio dir
#     if not os.path.exists(settings.AUDIO_DIR):
#         os.makedirs(settings.AUDIO_DIR)

#     video_name = os.path.basename(video_path).split('.')[0]
#     audio_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_instructions.mp3")
#     text_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_instructions.txt")

#     # Save script for reference
#     with open(text_filename, "w") as f:
#         f.write(script_text)

#     # Generate audio with a clear voice
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="alloy",
#         input=script_text,
#         speed=0.95  # Slightly slower for clarity
#     )

#     with open(audio_filename, "wb") as f:
#         f.write(response.read())

#     return audio_filename, script_text


# # ------------------------------------------------------
# # 4. Full pipeline for exercise instructions
# # ------------------------------------------------------
# def process_video_for_exercise_instructions(video_path):
#     """
#     End-to-end: Extract frames → Build exercise script → Generate audio
#     """
#     # Extract key frames
#     frame_paths = extract_keyframes(video_path, max_frames=12)
#     if not frame_paths or len(frame_paths) < 3:
#         raise ValueError("Not enough frames extracted to provide proper instructions")

#     # Step 1: Get frame-level exercise cues
#     frame_instructions = generate_frame_instructions(frame_paths)

#     # Step 2: Create step-by-step exercise script
#     script_text = generate_coaching_script(frame_instructions)

#     # Step 3: Generate clear audio instructions
#     audio_filename, final_script = generate_instruction_audio(script_text, video_path)

#     # Cleanup
#     for path in frame_paths:
#         if os.path.exists(path):
#             os.remove(path)

#     return audio_filename, final_script

#working fine 


# from openai import OpenAI
# import base64
# import json
# import os
# import cv2
# from app.core.config import settings
# from app.services.video_processor import extract_keyframes

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# # ------------------------------------------------------
# # 1. Frame-level instruction extraction for beginners
# # ------------------------------------------------------
# def generate_frame_instructions(frame_paths):
#     """
#     Generate beginner-friendly, actionable cues for each frame
#     """
#     instructions = []

#     for image_path in frame_paths:
#         with open(image_path, "rb") as image_file:
#             base64_image = base64.b64encode(image_file.read()).decode("utf-8")

#         prompt = """
#         Analyze this exercise frame and provide clear, beginner-friendly instructions.
        
#         Focus on:
#         1. What body position should be achieved in this frame
#         2. Key form points for proper technique
#         3. Breathing guidance for this phase
#         4. If specific limbs are moving, specify which ones (left/right arm/leg)
        
#         Example: "Lower into position, keeping your chest up and knees behind toes. Inhale as you descend."
#         Example with specific limbs: "Step forward with your right leg, keeping your knee aligned with your ankle."
#         """

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {"type": "image_url",
#                          "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
#                          }
#                     ],
#                 }
#             ],
#             max_tokens=120,
#             temperature=0.2,
#         )

#         instructions.append(response.choices[0].message.content.strip())

#     return instructions

# # ------------------------------------------------------
# # 2. Create step-by-step exercise guide
# # ------------------------------------------------------
# def generate_coaching_script(frame_instructions):
#     """
#     Create a step-by-step guide for this exercise
#     """
#     prompt = f"""
#     Create a step-by-step guide for this exercise based on these frame instructions:
    
#     {json.dumps(frame_instructions, indent=2)}
    
#     Structure your guide as follows:
#     1. Explain the starting position in detail
#     2. Break down the movement phase by phase
#     3. Include breathing cues throughout
#     4. End with how to properly finish the exercise
    
#     IMPORTANT: Be specific about which limbs to move when necessary. If the exercise involves 
#     alternating sides or specific limb movements, clearly indicate which arm/leg to use.
    
#     Speak directly to the listener with clear, actionable instructions.
#     Use simple language and focus only on what to do, not why.
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system",
#              "content": "You are a fitness trainer giving direct exercise instructions. Be specific about limb movements when needed."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=800,
#         temperature=0.3,
#     )

#     return response.choices[0].message.content.strip()


# # ------------------------------------------------------
# # 3. Convert script into clear audio
# # ------------------------------------------------------
# def generate_instruction_audio(script_text, video_path):
#     """
#     Convert coaching script into clear audio instructions
#     """
#     # Create audio dir
#     if not os.path.exists(settings.AUDIO_DIR):
#         os.makedirs(settings.AUDIO_DIR)

#     video_name = os.path.basename(video_path).split('.')[0]
#     audio_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_instructions.mp3")
#     text_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_instructions.txt")

#     # Save script for reference
#     with open(text_filename, "w") as f:
#         f.write(script_text)

#     # Generate audio with a clear voice
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="alloy",
#         input=script_text,
#         speed=0.95  # Slightly slower for clarity
#     )

#     with open(audio_filename, "wb") as f:
#         f.write(response.read())

#     return audio_filename, script_text


# # ------------------------------------------------------
# # 4. Full pipeline for exercise instructions
# # ------------------------------------------------------
# def process_video_for_exercise_instructions(video_path):
#     """
#     End-to-end: Extract frames → Build exercise script → Generate audio
#     """
#     # Extract key frames
#     frame_paths = extract_keyframes(video_path, max_frames=12)
#     if not frame_paths or len(frame_paths) < 3:
#         raise ValueError("Not enough frames extracted to provide proper instructions")

#     # Step 1: Get frame-level exercise cues
#     frame_instructions = generate_frame_instructions(frame_paths)

#     # Step 2: Create step-by-step exercise script
#     script_text = generate_coaching_script(frame_instructions)

#     # Step 3: Generate clear audio instructions
#     audio_filename, final_script = generate_instruction_audio(script_text, video_path)

#     # Cleanup
#     for path in frame_paths:
#         if os.path.exists(path):
#             os.remove(path)

#     return audio_filename, final_script

## same as first


from openai import OpenAI
import base64
import json
import os
import cv2
from app.core.config import settings
from app.services.video_processor import extract_keyframes

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ------------------------------------------------------
# 1. Enhanced frame-level instruction extraction
# ------------------------------------------------------
def generate_detailed_frame_instructions(frame_paths):
    """
    Generate comprehensive exercise instructions for each frame suitable for all levels
    """
    instructions = []

    for i, image_path in enumerate(frame_paths):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        prompt = """
        Analyze this exercise frame and describe ONLY the main action being performed.
Keep it short, clear, and instructional.
Focus only on body movement and positioning needed to do the exercise correctly.
Do not add beginner/advanced variations, breathing, or mistakes to avoid.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                         }
                    ],
                }
            ],
            max_tokens=250,
            temperature=0.2,
        )

        instructions.append({
            "frame_number": i + 1,
            "description": response.choices[0].message.content.strip()
        })

    return instructions


# ------------------------------------------------------
# 2. Create comprehensive step-by-step exercise guide
# ------------------------------------------------------
def generate_comprehensive_coaching_script(frame_instructions, video_duration):
    """
    Create a detailed step-by-step guide suitable for all skill levels
    """
    prompt = f"""
Create a simple, step-by-step exercise instruction based only on these frame descriptions:
    
    {json.dumps(frame_instructions, indent=2)}
    
    Video duration: {video_duration} seconds

Guidelines:
- Keep the guide short and clear
- Describe only how to perform the exercise shown
- Focus on the actual movement and body positioning
- Exclude breathing tips, beginner/advanced variations, or common mistakes
- Write it as spoken coaching instructions
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are an expert fitness instructor who creates comprehensive exercise guides suitable for all skill levels."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


# ------------------------------------------------------
# 3. Convert comprehensive script into clear audio
# ------------------------------------------------------
def generate_comprehensive_audio(script_text, video_path):
    """
    Convert detailed coaching script into clear audio instructions
    """
    # Create audio dir
    if not os.path.exists(settings.AUDIO_DIR):
        os.makedirs(settings.AUDIO_DIR)

    video_name = os.path.basename(video_path).split('.')[0]
    audio_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_comprehensive_instructions.mp3")
    text_filename = os.path.join(settings.AUDIO_DIR, f"{video_name}_comprehensive_instructions.txt")

    # Save script for reference
    with open(text_filename, "w") as f:
        f.write(script_text)

    # Generate audio with a clear, instructional voice
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",  # Clear and professional
        input=script_text,
        speed=0.92  # Slightly slower for comprehensive instructions
        
    )

    with open(audio_filename, "wb") as f:
        f.write(response.read())

    return audio_filename, script_text


# ------------------------------------------------------
# 4. Get video duration
# ------------------------------------------------------
def get_video_duration(video_path):
    """
    Extract video duration in seconds
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    cap.release()
    return int(duration)


# ------------------------------------------------------
# 5. Full pipeline for comprehensive exercise instructions
# ------------------------------------------------------
def process_video_for_comprehensive_instructions(video_path):
    """
    End-to-end: Extract frames → Build comprehensive script → Generate audio
    """
    # Get video duration
    video_duration = get_video_duration(video_path)
    
    # Extract key frames (slightly more for comprehensive guide)
    frame_paths = extract_keyframes(video_path, max_frames=15)
    if not frame_paths or len(frame_paths) < 3:
        raise ValueError("Not enough frames extracted to provide proper instructions")

    # Step 1: Get detailed frame-level exercise cues
    frame_instructions = generate_detailed_frame_instructions(frame_paths)

    # Step 2: Create comprehensive step-by-step exercise script
    script_text = generate_comprehensive_coaching_script(frame_instructions, video_duration)

    # Step 3: Generate detailed audio instructions
    audio_filename, final_script = generate_comprehensive_audio(script_text, video_path)

    # Cleanup
    for path in frame_paths:
        if os.path.exists(path):
            os.remove(path)

    return audio_filename, final_script


# ------------------------------------------------------
# 6. Backward compatibility function
# ------------------------------------------------------
def process_video_for_audio(video_path):
    """
    Alias for backward compatibility
    """
    return process_video_for_comprehensive_instructions(video_path)