# import cv2
# import uuid
# import os
# from app.core.config import settings

# def extract_keyframes(video_path, frame_interval=30):
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
#     saved_frames = []

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_count % frame_interval == 0:
#             frame_filename = os.path.join(settings.UPLOAD_DIR, f"frame_{uuid.uuid4().hex}.jpg")
#             cv2.imwrite(frame_filename, frame)
#             saved_frames.append(frame_filename)

#         frame_count += 1

#     cap.release()
#     return saved_frames

# import cv2
# import uuid
# import os
# import numpy as np
# from app.core.config import settings

# def extract_keyframes(video_path, max_frames=10):
#     cap = cv2.VideoCapture(video_path)
#     saved_frames = []
#     prev_frame = None
#     frame_count = 0
    
#     # Get video properties
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     duration = total_frames / fps if fps > 0 else 0
    
#     # Adjust sampling based on video length
#     if duration > 30:  # Longer videos need more sparse sampling
#         frame_interval = max(15, int(total_frames / 20))
#     else:
#         frame_interval = 10
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
            
#         # Convert to grayscale for motion detection
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
#         if prev_frame is None:
#             prev_frame = gray
#             continue
            
#         # Calculate frame difference for motion detection
#         frame_delta = cv2.absdiff(prev_frame, gray)
#         thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
#         thresh = cv2.dilate(thresh, None, iterations=2)
        
#         # Check if there's significant motion
#         motion_percentage = np.sum(thresh) / (thresh.size * 255)
        
#         # Save frame if there's significant motion or at regular intervals
#         if motion_percentage > 0.1 or frame_count % frame_interval == 0:
#             frame_filename = os.path.join(settings.UPLOAD_DIR, f"frame_{uuid.uuid4().hex}.jpg")
#             cv2.imwrite(frame_filename, frame)
#             saved_frames.append(frame_filename)
            
#             if len(saved_frames) >= max_frames:
#                 break
        
#         prev_frame = gray
#         frame_count += 1

#     # If no frames with motion were found, take evenly spaced frames
#     if not saved_frames:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to beginning
#         frame_interval = max(1, total_frames // max_frames)
        
#         for i in range(max_frames):
#             pos = i * frame_interval
#             cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
#             ret, frame = cap.read()
#             if ret:
#                 frame_filename = os.path.join(settings.UPLOAD_DIR, f"frame_{uuid.uuid4().hex}.jpg")
#                 cv2.imwrite(frame_filename, frame)
#                 saved_frames.append(frame_filename)

#     cap.release()
#     return saved_frames

## work but frame is short

import cv2
import uuid
import os
import numpy as np
from app.core.config import settings

# def extract_keyframes(video_path, max_frames=12):  # Increased max_frames

#     cap = cv2.VideoCapture(video_path)
#     saved_frames = []
    
#     # Get video properties
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     duration = total_frames / fps if fps > 0 else 0
    
#     print(f"Video duration: {duration:.2f} seconds, Total frames: {total_frames}, FPS: {fps}")
    
#     # Adaptive frame extraction based on video duration
#     if duration <= 1:  # Very short videos (<1s)
#         # Capture all frames for very short videos
#         max_frames = min(15, total_frames)
#         frame_interval = 1
#     elif duration <= 5:  # Short videos (1-5s)
#         max_frames = 10  # More frames for short videos
#         frame_interval = max(1, total_frames // max_frames)
#     elif duration <= 15:  # Medium videos (5-15s) - like your 8s videos
#         max_frames = 12  # Increased frames for better analysis
#         frame_interval = max(1, total_frames // max_frames)
#     else:  # Longer videos (>15s)
#         frame_interval = max(1, total_frames // max_frames)
    
#     # For videos in the 5-15 second range, use a hybrid approach
#     if 5 <= duration <= 15:
#         # Use motion detection for key moments but ensure we get enough frames
#         prev_frame = None
#         motion_frames = []
#         frame_count = 0
        
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
                
#             # Always capture first, middle, and last frames
#             if frame_count == 0 or frame_count == total_frames // 2 or frame_count == total_frames - 1:
#                 frame_filename = os.path.join(settings.UPLOAD_DIR, f"frame_{uuid.uuid4().hex}_{frame_count}.jpg")
#                 cv2.imwrite(frame_filename, frame)
#                 saved_frames.append(frame_filename)
            
#             # Motion detection for additional frames
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
#             if prev_frame is None:
#                 prev_frame = gray
#                 frame_count += 1
#                 continue
                
#             # Calculate frame difference for motion detection
#             frame_delta = cv2.absdiff(prev_frame, gray)
#             thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
#             thresh = cv2.dilate(thresh, None, iterations=2)
            
#             # Check if there's significant motion
#             motion_percentage = np.sum(thresh) / (thresh.size * 255)
            
#             # Save frame if there's significant motion
#             if motion_percentage > 0.08:  # Lower threshold to capture more motion
#                 frame_filename = os.path.join(settings.UPLOAD_DIR, f"motion_{uuid.uuid4().hex}_{frame_count}.jpg")
#                 cv2.imwrite(frame_filename, frame)
#                 motion_frames.append((frame_count, frame_filename, motion_percentage))
            
#             prev_frame = gray
#             frame_count += 1
        
#         # Sort motion frames by motion intensity and select top ones
#         motion_frames.sort(key=lambda x: x[2], reverse=True)
#         for _, frame_path, _ in motion_frames[:min(6, len(motion_frames))]:
#             if len(saved_frames) < max_frames and frame_path not in saved_frames:
#                 saved_frames.append(frame_path)
        
#         # If we still don't have enough frames, add evenly spaced ones
#         if len(saved_frames) < max_frames:
#             additional_frames_needed = max_frames - len(saved_frames)
#             additional_interval = max(1, total_frames // additional_frames_needed)
            
#             for i in range(additional_frames_needed):
#                 pos = i * additional_interval
#                 if pos < total_frames:
#                     cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
#                     ret, frame = cap.read()
#                     if ret:
#                         frame_filename = os.path.join(settings.UPLOAD_DIR, f"additional_{uuid.uuid4().hex}_{pos}.jpg")
#                         cv2.imwrite(frame_filename, frame)
#                         if frame_filename not in saved_frames:
#                             saved_frames.append(frame_filename)
#     else:
#         # For other video lengths, use the standard approach
#         frame_count = 0
#         while frame_count < total_frames:
#             ret, frame = cap.read()
#             if not ret:
#                 break
                
#             # Capture frames at regular intervals
#             if frame_count % frame_interval == 0:
#                 frame_filename = os.path.join(settings.UPLOAD_DIR, f"frame_{uuid.uuid4().hex}_{frame_count}.jpg")
#                 cv2.imwrite(frame_filename, frame)
#                 saved_frames.append(frame_filename)
                
#                 if len(saved_frames) >= max_frames:
#                     break
            
#             frame_count += 1
    
#     # Ensure we have key frames: start, middle, and end of movement
#     if saved_frames and total_frames > 1:
#         # Always include first frame
#         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         ret, frame = cap.read()
#         if ret:
#             first_frame_path = os.path.join(settings.UPLOAD_DIR, f"first_{uuid.uuid4().hex}.jpg")
#             cv2.imwrite(first_frame_path, frame)
#             if first_frame_path not in saved_frames:
#                 saved_frames.append(first_frame_path)
        
#         # Always include middle frame
#         mid_point = total_frames // 2
#         cap.set(cv2.CAP_PROP_POS_FRAMES, mid_point)
#         ret, frame = cap.read()
#         if ret:
#             mid_frame_path = os.path.join(settings.UPLOAD_DIR, f"mid_{uuid.uuid4().hex}.jpg")
#             cv2.imwrite(mid_frame_path, frame)
#             if mid_frame_path not in saved_frames:
#                 saved_frames.append(mid_frame_path)
        
#         # Always include last frame
#         cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
#         ret, frame = cap.read()
#         if ret:
#             last_frame_path = os.path.join(settings.UPLOAD_DIR, f"last_{uuid.uuid4().hex}.jpg")
#             cv2.imwrite(last_frame_path, frame)
#             if last_frame_path not in saved_frames:
#                 saved_frames.append(last_frame_path)
    
#     cap.release()
    
#     # Limit to max_frames if we have too many
#     if len(saved_frames) > max_frames:
#         # Select a diverse set of frames
#         selected_frames = []
#         step = len(saved_frames) // max_frames
#         for i in range(0, len(saved_frames), step):
#             if len(selected_frames) < max_frames:
#                 selected_frames.append(saved_frames[i])
#             else:
#                 # Remove the extra frames
#                 os.remove(saved_frames[i])
#         saved_frames = selected_frames
    
#     print(f"Extracted {len(saved_frames)} frames from video")
#     return saved_frames



def extract_keyframes(video_path, max_frames=16):  # Increased for better coverage
    cap = cv2.VideoCapture(video_path)
    saved_frames = []
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video duration: {duration:.2f} seconds, Total frames: {total_frames}, FPS: {fps}")
    
    # Capture frames at strategic points for full body analysis
    key_positions = []
    
    # Always capture start, quarter, half, three-quarter, and end points
    key_positions.extend([0, total_frames // 4, total_frames // 2, 
                        3 * total_frames // 4, total_frames - 1])
    
    # Add more positions for longer videos
    if duration > 10:
        additional_positions = 8
        for i in range(1, additional_positions):
            pos = i * total_frames // additional_positions
            key_positions.append(pos)
    
    # Remove duplicates and sort
    key_positions = sorted(set([p for p in key_positions if p < total_frames]))
    
    # Capture frames at key positions
    for pos in key_positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if ret:
            frame_filename = os.path.join(settings.UPLOAD_DIR, f"fullbody_{uuid.uuid4().hex}_{pos}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frames.append(frame_filename)
    
    # Additional motion-based frames for movement analysis
    prev_frame = None
    motion_frames = []
    frame_count = 0
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if prev_frame is not None:
            frame_delta = cv2.absdiff(prev_frame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            motion_score = np.sum(thresh) / (thresh.size * 255)
            if motion_score > 0.08:  # Lower threshold to capture more movement phases
                motion_frames.append((frame_count, frame.copy(), motion_score))
        
        prev_frame = gray
        frame_count += 1
    
    # Select diverse motion frames
    motion_frames.sort(key=lambda x: x[2], reverse=True)
    motion_frames = motion_frames[:min(8, len(motion_frames))]  # Select top motion frames
    
    # Ensure diversity across the timeline
    timeline_segments = 4
    segment_size = total_frames // timeline_segments
    selected_motion_frames = []
    
    for segment in range(timeline_segments):
        segment_start = segment * segment_size
        segment_end = (segment + 1) * segment_size
        
        # Get motion frames in this segment
        segment_frames = [f for f in motion_frames if segment_start <= f[0] < segment_end]
        if segment_frames:
            # Take the highest motion frame from this segment
            segment_frames.sort(key=lambda x: x[2], reverse=True)
            selected_motion_frames.append(segment_frames[0])
    
    # Save selected motion frames
    for frame_count, frame, score in selected_motion_frames:
        if len(saved_frames) < max_frames:
            frame_filename = os.path.join(settings.UPLOAD_DIR, f"motion_{uuid.uuid4().hex}_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frames.append(frame_filename)
    
    cap.release()
    
    # Ensure we have enough frames
    if len(saved_frames) < max_frames:
        additional_needed = max_frames - len(saved_frames)
        additional_interval = max(1, total_frames // additional_needed)
        
        cap = cv2.VideoCapture(video_path)
        for i in range(additional_needed):
            pos = i * additional_interval
            if pos < total_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                ret, frame = cap.read()
                if ret:
                    frame_filename = os.path.join(settings.UPLOAD_DIR, f"additional_{uuid.uuid4().hex}_{pos}.jpg")
                    cv2.imwrite(frame_filename, frame)
                    saved_frames.append(frame_filename)
        cap.release()
    
    print(f"Extracted {len(saved_frames)} frames for comprehensive whole-body analysis")
    return saved_frames