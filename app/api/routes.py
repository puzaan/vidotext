# import os
# import uuid
# import shutil
# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import JSONResponse
# from app.core.config import settings
# from app.services.video_processor import extract_keyframes
# from app.services.openai_service import generate_description_from_images

# router = APIRouter()

# @router.post("/analyze-exercise", summary="Analyze Exercise Video", tags=["Video Analyzer"])
# async def analyze_exercise_video(file: UploadFile = File(...)):
#     try:
#         file_ext = file.filename.split('.')[-1]
#         video_filename = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4().hex}.{file_ext}")

#         with open(video_filename, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#         frame_paths = extract_keyframes(video_filename, frame_interval=30)
#         descriptions = generate_description_from_images(frame_paths)

#         os.remove(video_filename)
#         for path in frame_paths:
#             os.remove(path)

#         return JSONResponse(content={"descriptions": descriptions})

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})


# import os
# import uuid
# import shutil
# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import JSONResponse
# from app.core.config import settings
# from app.services.video_processor import extract_keyframes
# from app.services.openai_service import generate_description_from_images

# router = APIRouter()

# @router.post("/analyze-exercise", summary="Analyze Exercise Video", tags=["Video Analyzer"])
# async def analyze_exercise_video(file: UploadFile = File(...)):
#     try:
#         # Validate file type
#         if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
#             return JSONResponse(
#                 status_code=400, 
#                 content={"error": "Invalid file format. Please upload a video file."}
#             )
        
#         file_ext = file.filename.split('.')[-1]
#         video_filename = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4().hex}.{file_ext}")

#         # Save the uploaded file
#         with open(video_filename, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#         # Extract keyframes
#         frame_paths = extract_keyframes(video_filename, frame_interval=30)
        
#         if not frame_paths:
#             os.remove(video_filename)
#             return JSONResponse(
#                 status_code=400, 
#                 content={"error": "Could not extract frames from video. The file might be corrupted."}
#             )
        
#         # Generate descriptions
#         descriptions = generate_description_from_images(frame_paths)
        
#         # Clean up
#         os.remove(video_filename)
#         for path in frame_paths:
#             os.remove(path)

#         # Combine all descriptions into a comprehensive analysis
#         combined_prompt = """
#         I have multiple descriptions of different frames from the same exercise video. 
#         Please analyze all these descriptions and create a comprehensive analysis including:
        
#         1. Exercise name and type
#         2. Complete step-by-step instructions
#         3. All muscles targeted
#         4. All benefits
#         5. Common mistakes and precautions
#         6. Variations or progressions (if visible)
        
#         Here are the individual frame descriptions:
#         """ + "\n\n".join([f"Frame {i+1}: {desc}" for i, desc in enumerate(descriptions)])
        
#         # Get final comprehensive analysis
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a fitness expert and personal trainer."},
#                 {"role": "user", "content": combined_prompt}
#             ],
#             max_tokens=1500,
#             temperature=0.2,
#         )
        
#         final_analysis = response.choices[0].message.content

#         return JSONResponse(content={
#             "analysis": final_analysis,
#             "frame_count": len(frame_paths)
#         })

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

# import os
# import uuid
# import shutil
# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import JSONResponse
# from app.core.config import settings
# from app.services.video_processor import extract_keyframes
# from app.services.openai_service import generate_individual_descriptions, generate_combined_analysis

# router = APIRouter()

# @router.post("/analyze-exercise", summary="Analyze Exercise Video", tags=["Video Analyzer"])
# async def analyze_exercise_video(file: UploadFile = File(...)):
#     try:
#         # Validate file type
#         if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
#             return JSONResponse(
#                 status_code=400, 
#                 content={"error": "Invalid file format. Please upload a video file."}
#             )
        
#         file_ext = file.filename.split('.')[-1]
#         video_filename = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4().hex}.{file_ext}")

#         # Save the uploaded file
#         with open(video_filename, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#         # Extract keyframes
#         frame_paths = extract_keyframes(video_filename, max_frames=8)
        
#         if not frame_paths:
#             os.remove(video_filename)
#             return JSONResponse(
#                 status_code=400, 
#                 content={"error": "Could not extract frames from video. The file might be corrupted or too short."}
#             )
        
#         # Generate individual descriptions for each frame
#         individual_descriptions = generate_individual_descriptions(frame_paths)
        
#         # Combine all descriptions into a comprehensive analysis
#         comprehensive_analysis = generate_combined_analysis(individual_descriptions)

#         # Clean up
#         os.remove(video_filename)
#         for path in frame_paths:
#             os.remove(path)

#         return comprehensive_analysis

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

## work fine but short image frame
import os
import uuid
import shutil
import logging
from fastapi import APIRouter, UploadFile, File,HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from app.core.config import settings
from app.services.video_processor import extract_keyframes
from app.services.openai_service import generate_individual_descriptions, generate_combined_analysis
from app.services.audio_service import generate_instruction_audio  # Updated import - removed get_video_duration


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze-exercise", summary="Analyze Exercise Video", tags=["Video Analyzer"])
async def analyze_exercise_video(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            return JSONResponse(
                status_code=400, 
                content={"error": "Invalid file format. Please upload a video file."}
            )
        
        file_ext = file.filename.split('.')[-1]
        video_filename = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4().hex}.{file_ext}")

        # Save the uploaded file
        with open(video_filename, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract keyframes with improved logic for 8-second videos
        frame_paths = extract_keyframes(video_filename, max_frames=12)  # Increased to 12 frames
        
        logger.info(f"Extracted {len(frame_paths)} frames from video")
        
        if not frame_paths or len(frame_paths) < 3:  # Require at least 3 frames
            if os.path.exists(video_filename):
                os.remove(video_filename)
            for path in frame_paths:
                if os.path.exists(path):
                    os.remove(path)
                    
            return JSONResponse(
                status_code=400, 
                content={"error": f"Could not extract enough frames from video ({len(frame_paths)} extracted). The file might be corrupted or too short."}
            )
        
        # Generate individual descriptions for each frame
        individual_descriptions = generate_individual_descriptions(frame_paths)
        
        # Combine all descriptions into a comprehensive analysis
        comprehensive_analysis = generate_combined_analysis(individual_descriptions)

        # Clean up
        if os.path.exists(video_filename):
            os.remove(video_filename)
        for path in frame_paths:
            if os.path.exists(path):
                os.remove(path)

        return comprehensive_analysis

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        # Clean up any remaining files
        if 'video_filename' in locals() and os.path.exists(video_filename):
            os.remove(video_filename)
        if 'frame_paths' in locals():
            for path in frame_paths:
                if os.path.exists(path):
                    os.remove(path)
                    
        return JSONResponse(status_code=500, content={"error": str(e)})
    


@router.post("/generate-audio-instructions", summary="Generate exercise instructions audio", tags=["Audio Instructions"])
async def generate_audio_instructions(file: UploadFile = File(...)):
    """
    Generate audio instructions that exactly match the video duration
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a video file.")
        
        file_ext = file.filename.split('.')[-1]
        video_filename = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4().hex}.{file_ext}")

        # Save the uploaded file
        with open(video_filename, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Generate audio instructions directly from video
        audio_filename, audio_duration, instructions_text = generate_instruction_audio(video_filename)

        # Clean up video file
        if os.path.exists(video_filename):
            os.remove(video_filename)

        return {
            "audio_duration": audio_duration,
            "audio_url": f"/audio/{os.path.basename(audio_filename)}",
            "text_url": f"/audio/{os.path.basename(audio_filename.replace('.mp3', '.txt'))}",
            "message": "Audio instructions generated successfully. Duration matches video length."
        }

    except Exception as e:
        logger.error(f"Error generating audio instructions: {str(e)}")
        # Clean up any remaining files
        if 'video_filename' in locals() and os.path.exists(video_filename):
            os.remove(video_filename)
                    
        raise HTTPException(status_code=500, detail=f"Error generating audio instructions: {str(e)}")






