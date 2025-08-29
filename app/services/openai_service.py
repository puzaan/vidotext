# from openai import OpenAI
# from app.core.config import settings

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# def generate_description_from_images(image_paths):
#     descriptions = []
#     for image_path in image_paths:
#         with open(image_path, "rb") as image_file:
#             prompt = (
#                 "You are a fitness expert. Describe the body exercise shown in the image. "
#                 "Since I can't send images via this API, imagine the exercise is shown here."
#             )
            
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 temperature=0.2,
#                 messages=[
#                     {"role": "system", "content": "You are a fitness expert."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=200,
#             )
            
#             description = response.choices[0].message.content
#             descriptions.append(description)
#     return descriptions


# from openai import OpenAI
# import base64
# from app.core.config import settings

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# def generate_description_from_images(image_paths):
#     descriptions = []
    
#     for image_path in image_paths:
#         # Encode image to base64
#         with open(image_path, "rb") as image_file:
#             base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
#         # Create the prompt
#         prompt = """
#         Analyze this exercise image and provide:
#         1. Name of the exercise
#         2. Step-by-step instructions on how to perform it correctly
#         3. Primary muscles targeted
#         4. Benefits of this exercise
#         5. Any precautions or common mistakes to avoid
        
#         Please structure your response clearly with these sections.
#         """
        
#         # Call OpenAI API with the image
#         response = client.chat.completions.create(
#             model="gpt-4o",  # Make sure you have access to this model
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{base64_image}"
#                             },
#                         },
#                     ],
#                 }
#             ],
#             max_tokens=1000,
#             temperature=0.2,
#         )
        
#         description = response.choices[0].message.content
#         descriptions.append(description)
    
#     return descriptions


from openai import OpenAI
import base64
from app.core.config import settings
import json

# Create a function to get the client
def get_openai_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def detect_gender_from_frames(image_paths):
    """Detect if the person in the video is male or female"""
    client = get_openai_client()
    
    # Use the first frame to detect gender
    if image_paths:
        with open(image_paths[0], "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = """
        Look at this person in the exercise video and determine:
        1. Is this person male or female? (Answer with just one word: male, female, or unclear)
        2. What is their approximate age range? (teen, young adult, adult, middle-aged, senior)
        
        Be objective and focus on observable characteristics.
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
            max_tokens=100,
            temperature=0.1,
        )
        
        result = response.choices[0].message.content.lower()
        if "female" in result:
            return "female"
        elif "male" in result:
            return "male"
    
    return "unclear"

# def generate_individual_descriptions(image_paths):
#     client = get_openai_client()
#     descriptions = []
    
#     for image_path in image_paths:
#         with open(image_path, "rb") as image_file:
#             base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
#         prompt = """
#         As a fitness expert, analyze this exercise frame and describe:
#         1. What exercise this appears to be
#         2. What phase of the movement is shown (starting position, mid-movement, completion)
#         3. Key muscles being engaged
#         4. Any equipment visible
#         5. Form observations (good form or potential issues)
        
#         Be specific and detailed in your analysis.
#         """
        
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{base64_image}"
#                             },
#                         },
#                     ],
#                 }
#             ],
#             max_tokens=400,
#             temperature=0.2,
#         )
        
#         descriptions.append(response.choices[0].message.content)
    
#     return descriptions

# def generate_combined_analysis(descriptions):
#     client = get_openai_client()

#     detected_gender = "unclear"
#     for desc in descriptions:
#         if "female" in desc.lower():
#             detected_gender = "female"
#             break
#         elif "male" in desc.lower():
#             detected_gender = "male"
#             break
    
#     # Combine all descriptions into a comprehensive analysis
#     combined_prompt = """
#     You are a professional fitness trainer. I have multiple descriptions of different frames from the same exercise video. 
#     Please analyze all these descriptions and create a comprehensive exercise analysis including:
    
#     {
#   "Exercise Name and Type": "Squat, Compound Lower Body Exercise",
#   "Step-by-Step Instructions": [
#     "Step 1: Position your feet shoulder-width apart.",
#     "Step 2: Keep your back straight and chest up.",
#     "Step 3: Lower your body by bending your knees and hips.",
#     "Step 4: Stop when your thighs are parallel to the ground.",
#     "Step 5: Push through your heels to return to the starting position."
#   ],
#   "Primary Muscles Targeted": ["Quadriceps", "Glutes", "Hamstrings"],
#   "Secondary Muscles Targeted": ["Core", "Calves"],
#   "Benefits": [
#     "Strengthens lower body muscles.",
#     "Improves flexibility and balance.",
#     "Increases mobility in the hips and knees."
#   ],
#   "Common Mistakes": [
#     {
#       "Mistake": "Knees caving inward",
#       "Correction": "Push your knees outward to align with your toes."
#     },
#     {
#       "Mistake": "Leaning too far forward",
#       "Correction": "Keep your chest up and engage your core."
#     }
#   ],
#   "Equipment Needed": ["None", "Optional: Dumbbells or Barbell"],
#   "Difficulty Level": "Intermediate",
#   "Safety Precautions": [
#     "Ensure knees don't extend beyond toes.",
#     "Avoid using heavy weights if you're new to the exercise."
#   ],
#   "Contraindications": [
#     "Avoid if you have knee or back issues.",
#     "Consult a physician if you have joint problems."
#   ],
#   "Recommended Sets and Reps": {
#     "Beginner": "3 sets of 10-12 reps",
#     "Intermediate": "4 sets of 12-15 reps",
#     "Advanced": "5 sets of 15-20 reps"
#   },
#   "Variations or Progressions": [
#     "Add weights like dumbbells or a barbell.",
#     "Try single-leg squats for increased difficulty."
#   ],
#   "Suitable For": {
#     "Genders": ["male", "female"],  # or specific gender
#     "Fitness Levels": ["beginner", "intermediate", "advanced"],
#     "Age Groups": ["teens", "adults", "seniors"]  # with appropriate modifications
#   }
# }
#     The person in the video appears to be: {detected_gender}

#     Here are the individual frame descriptions from the video:
#     """ + "\n\n".join([f"FRAME {i+1} ANALYSIS:\n{desc}\n" for i, desc in enumerate(descriptions)]) + """
    
#     Please **ONLY** return a JSON response in the exact format above. No extra text, no explanations, and no other information.
#     """
    
#     # Get final comprehensive analysis
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system", 
#                 "content": "You are an expert fitness trainer with deep knowledge of exercise physiology, biomechanics, and training methodology. You understand gender differences in exercise programming and can provide appropriate recommendations."
#             },
#             {
#                 "role": "user", 
#                 "content": combined_prompt
#             }
#         ],
#         temperature=0.2,
#     )

#     # print(response.choices[0].message.content)

#     response_content  = response.choices[0].message.content

#     try:
#         response_json = json.loads(response_content.replace("```json", "").replace("```", ""))
#         print(response_json)
#         return response_json
#     except json.JSONDecodeError:
#         print("Failed to parse the response as JSON. Raw response:")
#         print(response_content)
#         return response_content


def generate_individual_descriptions(image_paths):
    client = get_openai_client()
    descriptions = []
    
    for i, image_path in enumerate(image_paths):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Comprehensive whole-body analysis prompt
        prompt = """
        As an expert exercise physiologist and biomechanics specialist, analyze this exercise frame with detailed attention to FULL BODY POSITIONING and form:
        
        CRITICAL ANALYSIS AREAS:
        
        1. FULL BODY ASSESSMENT:
           - Overall body alignment and posture
           - Spinal position (neutral, flexed, extended, rotated)
           - Hip and pelvic positioning
           - Lower body alignment (knees, ankles, feet)
           - Upper body positioning (shoulders, chest, head)
        
        2. JOINT ANGLES AND POSITIONS:
           - Shoulder joint angle and position
           - Elbow angle and position
           - Hip angle and positioning
           - Knee angle and alignment
           - Ankle and foot positioning
        
        3. MOVEMENT PHASE IDENTIFICATION:
           - Starting position, concentric phase, eccentric phase, or peak contraction
           - Range of motion assessment
           - Movement quality and control
        
        4. EXERCISE IDENTIFICATION:
           - Specific exercise name and variation
           - Primary movement pattern (push, pull, squat, hinge, etc.)
           - Equipment being used
        
        5. MUSCLE ENGAGEMENT ANALYSIS:
           - Primary muscles being targeted based on body position
           - Secondary and stabilizer muscles engaged
           - Muscle lengthening/shortening patterns
        
        6. FORM AND TECHNIQUE ASSESSMENT:
           - Excellent form observations
           - Potential technical errors or issues
           - Safety considerations based on body positioning
        
        7. INDIVIDUAL FACTORS:
           - Apparent gender and approximate age if discernible
           - Body type considerations if relevant
        
        Provide extremely detailed analysis of the ENTIRE body position and biomechanics.
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
            max_tokens=800,  # Increased for comprehensive whole-body analysis
            temperature=0.1,
        )
        
        descriptions.append(response.choices[0].message.content)
    
    return descriptions

def generate_combined_analysis(descriptions):
    client = get_openai_client()
    
    # Comprehensive whole-body analysis prompt
    combined_prompt = """
    You are an expert exercise physiologist and biomechanics specialist. Analyze all these frame descriptions and create a comprehensive exercise analysis with detailed attention to FULL BODY mechanics, form, and positioning.
    
    Pay special attention to:
    1. COMPLETE BODY ALIGNMENT and posture throughout the movement
    2. JOINT ANGLES and positions at different movement phases
    3. MUSCLE ENGAGEMENT patterns based on body positioning
    4. MOVEMENT QUALITY and technical execution
    5. EXERCISE-SPECIFIC biomechanical considerations
    
    Return analysis in this EXACT JSON format:
    
    {
      "Exercise Identification": {
        "Primary Exercise": "Assisted Chin-Up",
        "Specific Variation": "Reverse Wide Grip",
        "Movement Pattern": "Vertical Pull",
        "Equipment Used": ["Pull-up bar", "Resistance band"]
      },
      "Biomechanical Analysis": {
        "Starting Position": {
          "Body Alignment": "Full body hang with neutral spine",
          "Joint Angles": "Arms fully extended, shoulders packed",
          "Muscle Status": "Lats and biceps in stretched position"
        },
        "Mid-Movement": {
          "Body Alignment": "Maintained neutral spine, slight lean back",
          "Joint Angles": "Elbows flexed to 90 degrees, shoulders externally rotated",
          "Muscle Engagement": "Peak lat and biceps contraction"
        },
        "End Position": {
          "Body Alignment": "Chin over bar, chest elevated",
          "Joint Angles": "Elbows fully flexed, shoulders depressed",
          "Muscle Status": "Fully contracted upper back and arms"
        }
      },
      "Whole Body Form Assessment": {
        "Upper Body": {
          "Shoulder Position": "Properly packed and stable",
          "Elbow Alignment": "Tracking correctly without flare",
          "Chest Position": "Elevated and proud",
          "Head Position": "Neutral neck alignment"
        },
        "Core and Midsection": {
          "Spinal Alignment": "Maintained neutral spine throughout",
          "Core Engagement": "Appropriate bracing and stability",
          "Rib Cage Position": "Not flared, properly aligned"
        },
        "Lower Body": {
          "Hip Position": "Slight posterior tilt for stability",
          "Leg Alignment": "Straight with engaged glutes",
          "Foot Position": "Pointed or neutral, not swinging"
        }
      },
      "Muscle Engagement Analysis": {
        "Primary Muscles": ["Latissimus Dorsi", "Biceps Brachii", "Teres Major"],
        "Secondary Muscles": ["Rhomboids", "Trapezius", "Forearms"],
        "Stabilizer Muscles": ["Core muscles", "Glutes", "Shoulder stabilizers"],
        "Engagement Patterns": "Proper sequencing from lats to arms"
      },
      "Technical Execution": {
        "Range of Motion": "Full extension to chin over bar",
        "Tempo Control": "Controlled concentric and eccentric",
        "Form Quality": "Excellent technical execution",
        "Common Errors": ["Using momentum", "Incomplete range of motion"]
      },
      "Step-by-Step Instructions": [
        "Step 1: Set up with proper grip and body alignment",
        "Step 2: Engage core and depress shoulders",
        "Step 3: Initiate pull with back muscles",
        "Step 4: Continue pulling until chin clears bar",
        "Step 5: Lower with control maintaining form"
      ],
      "Benefits": [
        "Develops upper body pulling strength",
        "Improves back muscle development",
        "Enhances grip strength and endurance",
        "Builds core stability during pulling motions"
      ],
      "Progressions and Variations": [
        "Reduce assistance gradually",
        "Try different grip variations",
        "Add tempo variations for difficulty"
      ],
      "Safety Considerations": [
        "Maintain shoulder stability throughout",
        "Avoid kipping or swinging motions",
        "Ensure proper warm-up for shoulder health"
      ]
    }
    
    Here are the individual frame descriptions from the video:
    """ + "\n\n".join([f"FRAME {i+1} ANALYSIS:\n{desc}\n" for i, desc in enumerate(descriptions)]) + """
    
    CRITICAL: Provide extremely detailed analysis of the WHOLE BODY positioning, alignment, and biomechanics. Focus on how all body parts work together in the movement.
    
    Please **ONLY** return a JSON response in the exact format above. No extra text, no explanations, and no other information.
    """
    
    # Get final comprehensive analysis
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": "You are an expert exercise physiologist and biomechanics specialist with deep knowledge of full-body movement patterns, joint mechanics, and muscular engagement. You can analyze complete body positioning and provide detailed technical feedback."
            },
            {
                "role": "user", 
                "content": combined_prompt
            }
        ],
        temperature=0.1,
    )

    response_content = response.choices[0].message.content

    try:
        response_json = json.loads(response_content.replace("```json", "").replace("```", ""))
        print(response_json)
        return response_json
    except json.JSONDecodeError:
        print("Failed to parse the response as JSON. Raw response:")
        print(response_content)
        return response_content

# Keep the original function for backward compatibility
def generate_description_from_images(image_paths):
    individual_descriptions = generate_individual_descriptions(image_paths)
    return generate_combined_analysis(individual_descriptions)