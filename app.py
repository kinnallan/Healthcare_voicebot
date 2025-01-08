from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
import pyttsx3
import threading
import time
import json
from transformers import pipeline

app = Flask(__name__)

def load_health_advice():
    """Load health advice from JSON file"""
    try:
        with open('health_advice.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: health_advice.json file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in health_advice.json")
        return {}

def format_recommendations(recommendations):
    """Format recommendations into a readable string"""
    result = []
    for i, rec in enumerate(recommendations, 1):
        if isinstance(rec, dict):
            result.append(f"{i}. {rec['title']}")
            for item in rec['items']:
                result.append(f"   - {item}")
        else:
            result.append(f"{i}. {rec}")
    return "\n".join(result)

# Initialize text-to-speech engine
def init_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)  # Speed
    return engine

def speak(text):
    engine = init_engine()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak_threaded(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()
    thread.join()

def listen_for_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return None

def health_advice(text):
    """Provide health advice based on user input"""
    text = text.lower()
    
    # Load advice from JSON file
    advice_data = load_health_advice()
    
    # Check for matching condition
    for condition, data in advice_data.items():
        if condition in text:
            return f"{data['title']}\n{format_recommendations(data['recommendations'])}"
    
    return "I'm here to help with your health-related questions! Please ask me about specific symptoms or health conditions."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome', methods=['GET'])
def welcome():
    welcome_msg = "Welcome to Healthcare Voice Bot. How can I help you today?"
    speak_threaded(welcome_msg)
    return jsonify({"response": welcome_msg})

@app.route('/start_listening', methods=['GET'])
def start_listening():
    speak_threaded("I'm listening. Please tell me your health concern.")
    text = listen_for_input()
    
    if text:
        speak_threaded(f"You said: {text}")
        time.sleep(1)  # Short pause between speeches
        
        health_response = health_advice(text)
        speak_threaded(health_response)
        
        return jsonify({
            "input": text,
            "response": health_response
        })
    else:
        error_msg = "Sorry, I couldn't understand that. Could you please repeat?"
        speak_threaded(error_msg)
        return jsonify({
            "input": None,
            "response": error_msg
        })

@app.route('/stop_listening', methods=['GET'])
def stop_listening():
    goodbye_msg = "Thank you for using Healthcare Voice Bot. Take care!"
    speak_threaded(goodbye_msg)
    return jsonify({"response": goodbye_msg})

if __name__ == "__main__":
    app.run(debug=False, threaded=True, port=5001)
