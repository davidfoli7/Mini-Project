# from flask import Flask, request, jsonify, render_template
# import requests
# from flask_cors import CORS
# import speech_recognition as sr
# from gtts import gTTS
# import os
# import json

# app = Flask(__name__, template_folder='../backend/templates')
# CORS(app)

# # Replace this with your actual Google Gemini API key
# GOOGLE_GEMINI_API_KEY = "AIzaSyD40YUYIFIcievhralu1ySx9qFMO8PjS_s"
# API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_GEMINI_API_KEY}"

# def format_prompt(mode, prompt, **kwargs):
#     if mode == 'flashcards':
#         num_cards = kwargs.get('num_cards', 5)
#         return f"""Generate {num_cards} flashcards for the topic: {prompt}
# Format your response as a JSON array of objects with 'question' and 'answer' fields.
# Make the questions challenging but clear, and the answers concise but comprehensive.
# Example format:
# [
#     {{"question": "What is...", "answer": "It is..."}},
#     {{"question": "How does...", "answer": "It works by..."}}
# ]"""
    
#     elif mode == 'mcq':
#         num_questions = kwargs.get('num_questions', 5)
#         return f"""Generate {num_questions} multiple choice questions for the topic: {prompt}
# Format your response as a JSON array of objects with 'question', 'options' (array), and 'correct_answer' (index) fields.
# Make the questions challenging and ensure options are distinct and plausible.
# Example format:
# [
#     {{
#         "question": "What is...",
#         "options": ["Option A", "Option B", "Option C", "Option D"],
#         "correct_answer": 2
#     }}
# ]"""
    
#     elif mode == 'case_study':
#         return f"""Create a detailed case study about: {prompt}
# Format your response as a JSON object with the following structure:
# {{
#     "title": "Case Study: [Topic]",
#     "scenario": "Detailed description of the situation...",
#     "challenges": ["Challenge 1", "Challenge 2", ...],
#     "analysis": "In-depth analysis of the situation...",
#     "solution": "Proposed solution and approach...",
#     "learning_outcomes": ["Outcome 1", "Outcome 2", ...]
# }}"""
    
#     elif mode == 'summary':
#         return f"""Provide a comprehensive summary of: {prompt}
# Format your response as a JSON object with the following structure:
# {{
#     "main_points": ["Point 1", "Point 2", ...],
#     "key_concepts": ["Concept 1", "Concept 2", ...],
#     "summary": "Concise summary text...",
#     "additional_notes": ["Note 1", "Note 2", ...]
# }}"""
    
#     else:  # general Q&A
#         return prompt

# def validate_json_response(text, mode):
#     try:
#         data = json.loads(text)
#         if mode == 'flashcards':
#             if not isinstance(data, list) or not all(isinstance(card, dict) and 'question' in card and 'answer' in card for card in data):
#                 raise ValueError("Invalid flashcard format")
#         elif mode == 'mcq':
#             if not isinstance(data, list) or not all(isinstance(q, dict) and 'question' in q and 'options' in q and 'correct_answer' in q for q in data):
#                 raise ValueError("Invalid MCQ format")
#         elif mode == 'case_study':
#             required_fields = ['title', 'scenario', 'challenges', 'analysis', 'solution', 'learning_outcomes']
#             if not isinstance(data, dict) or not all(field in data for field in required_fields):
#                 raise ValueError("Invalid case study format")
#         elif mode == 'summary':
#             required_fields = ['main_points', 'key_concepts', 'summary', 'additional_notes']
#             if not isinstance(data, dict) or not all(field in data for field in required_fields):
#                 raise ValueError("Invalid summary format")
#         return data
#     except json.JSONDecodeError:
#         return None

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     data = request.json
#     prompt = data.get('prompt')
#     mode = data.get('mode', 'general')

#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400

#     formatted_prompt = format_prompt(
#         mode, 
#         prompt,
#         num_cards=data.get('num_cards', 5),
#         num_questions=data.get('num_questions', 5)
#     )

#     payload = {"contents": [{"parts": [{"text": formatted_prompt}]}]}
#     headers = {"Content-Type": "application/json"}

#     try:
#         response = requests.post(API_URL, json=payload, headers=headers)
#         response.raise_for_status()
        
#         answer = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
#         if mode in ['flashcards', 'mcq', 'case_study', 'summary']:
#             validated_response = validate_json_response(answer, mode)
#             if validated_response:
#                 return jsonify({"answer": json.dumps(validated_response)})
#             else:
#                 # If JSON validation fails, try to fix common formatting issues
#                 answer = answer.replace("```json", "").replace("```", "").strip()
#                 validated_response = validate_json_response(answer, mode)
#                 if validated_response:
#                     return jsonify({"answer": json.dumps(validated_response)})
#                 return jsonify({"error": "Invalid response format from AI"}), 500
        
#         return jsonify({"answer": answer})
    
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": f"Failed to fetch response from AI: {str(e)}"}), 500

# @app.route('/speech-to-text', methods=['POST'])
# def speech_to_text():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided"}), 400
    
#     audio_file = request.files['audio']
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.AudioFile(audio_file) as source:
#             audio = recognizer.record(source)
#             text = recognizer.recognize_google(audio)
#             return jsonify({"text": text})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/text-to-speech', methods=['POST'])
# def text_to_speech():
#     data = request.json
#     text = data.get('text')
    
#     if not text:
#         return jsonify({"error": "Text is required"}), 400
    
#     try:
#         tts = gTTS(text=text, lang='en')
#         audio_path = "static/audio/speech.mp3"
#         os.makedirs(os.path.dirname(audio_path), exist_ok=True)
#         tts.save(audio_path)
#         return jsonify({"audio_url": "/static/audio/speech.mp3"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=3002)





# new code


from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import speech_recognition as sr
from gtts import gTTS
import os
import json
from io import BytesIO
from pydub import AudioSegment

app = Flask(__name__, template_folder=os.path.abspath("backend/templates"))
CORS(app)

# Replace this with your actual Google Gemini API key
GOOGLE_GEMINI_API_KEY = "YOUR_API_KEY_HERE"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GOOGLE_GEMINI_API_KEY}"

def format_prompt(mode, prompt, **kwargs):
    if mode == 'flashcards':
        num_cards = kwargs.get('num_cards', 5)
        return f"""Generate {num_cards} flashcards for the topic: {prompt}
Format your response as a JSON array of objects with 'question' and 'answer' fields.
[
    {{"question": "What is...", "answer": "It is..."}},
    {{"question": "How does...", "answer": "It works by..."}}
]"""
    
    elif mode == 'mcq':
        num_questions = kwargs.get('num_questions', 5)
        return f"""Generate {num_questions} multiple choice questions for the topic: {prompt}
Format your response as a JSON array of objects with 'question', 'options' (array), and 'correct_answer' (index) fields.
[
    {{
        "question": "What is...",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": 2
    }}
]"""
    
    elif mode == 'case_study':
        return f"""Create a detailed case study about: {prompt}
Format your response as a JSON object with:
{{
    "title": "Case Study: [Topic]",
    "scenario": "Detailed description...",
    "challenges": ["Challenge 1", "Challenge 2"],
    "analysis": "Analysis...",
    "solution": "Proposed solution...",
    "learning_outcomes": ["Outcome 1", "Outcome 2"]
}}"""
    
    elif mode == 'summary':
        return f"""Provide a summary of: {prompt}
Format your response as:
{{
    "main_points": ["Point 1", "Point 2"],
    "key_concepts": ["Concept 1", "Concept 2"],
    "summary": "Summary text...",
    "additional_notes": ["Note 1", "Note 2"]
}}"""
    
    else:  # general Q&A
        return prompt

def validate_json_response(text, mode):
    try:
        data = json.loads(text)
        
        # If still a string, parse again
        if isinstance(data, str):
            data = json.loads(data)

        if mode == 'flashcards':
            if not isinstance(data, list) or not all(isinstance(card, dict) and 'question' in card and 'answer' in card for card in data):
                raise ValueError("Invalid flashcard format")
        elif mode == 'mcq':
            if not isinstance(data, list) or not all(isinstance(q, dict) and 'question' in q and 'options' in q and 'correct_answer' in q for q in data):
                raise ValueError("Invalid MCQ format")
        elif mode == 'case_study':
            required_fields = ['title', 'scenario', 'challenges', 'analysis', 'solution', 'learning_outcomes']
            if not isinstance(data, dict) or not all(field in data for field in required_fields):
                raise ValueError("Invalid case study format")
        elif mode == 'summary':
            required_fields = ['main_points', 'key_concepts', 'summary', 'additional_notes']
            if not isinstance(data, dict) or not all(field in data for field in required_fields):
                raise ValueError("Invalid summary format")
        
        return data
    except json.JSONDecodeError:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get('prompt')
    mode = data.get('mode', 'general')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    formatted_prompt = format_prompt(
        mode, 
        prompt,
        num_cards=data.get('num_cards', 5),
        num_questions=data.get('num_questions', 5)
    )

    payload = {"contents": [{"parts": [{"text": formatted_prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        response_json = response.json()
        candidates = response_json.get("candidates", [])

        if not candidates:
            return jsonify({"error": "No response from AI"}), 500

        answer = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        if not answer:
            return jsonify({"error": "Empty response from AI"}), 500

        if mode in ['flashcards', 'mcq', 'case_study', 'summary']:
            validated_response = validate_json_response(answer, mode)
            if validated_response:
                return jsonify({"answer": json.dumps(validated_response)})
            
            # Attempt to fix common JSON issues
            answer = answer.replace("```json", "").replace("```", "").strip()
            validated_response = validate_json_response(answer, mode)
            if validated_response:
                return jsonify({"answer": json.dumps(validated_response)})
            return jsonify({"error": "Invalid response format from AI"}), 500
        
        return jsonify({"answer": answer})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch response from AI: {str(e)}"}), 500

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    
    try:
        if audio_file.filename.endswith(".mp3"):
            audio = AudioSegment.from_file(audio_file, format="mp3")
            wav_buffer = BytesIO()
            audio.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            audio_file = wav_buffer  # Use converted file

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    try:
        tts = gTTS(text=text, lang='en')
        audio_dir = "static/audio"
        os.makedirs(audio_dir, exist_ok=True)
        audio_path = os.path.join(audio_dir, "speech.mp3")
        tts.save(audio_path)
        return jsonify({"audio_url": "/static/audio/speech.mp3"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3002)
