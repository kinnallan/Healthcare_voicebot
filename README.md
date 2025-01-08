# Healthcare_voicebot
The goal of this project is to create a Flask-based voice-activated healthcare assistant. The assistant will respond to users' spoken inquiries with basic health information and advice.

Features

Voice Recognition: Listens to user input and converts speech to text using speech_recognition.
Health Advice: Provides detailed health recommendations for common symptoms and conditions.
Text-to-Speech: Reads out responses to enhance the user experience using pyttsx3.
Web Interface: Simple web interface powered by Flask.
Modular Design: Easy to extend by adding more health advice or features.

File Structure

healthcare_voicebot/
|
|-- templates/
|   |-- index.html        # Main web interface
|
|-- app.py                # Flask application
|-- health_advice.json    # Health recommendations
|-- requirements.txt      # Python dependencies

Usage

Navigate to the web interface.
Click "Start Listening" to activate voice recognition.
Speak your health concern (e.g., "I have a headache").
Receive health advice in text and voice formats.

Technologies Used

Flask: Web framework for Python.
SpeechRecognition: For converting speech to text.
pyttsx3: Text-to-speech conversion.
JSON: For storing health advice data.
HTML: For creating the web interface.

To run
Open a terminal in the project directory.
Execute the command:
python app.py
Open your browser and visit http://127.0.0.1:5001/.
Interact with the bot via the web interface or voice commands.

Thank you for using Healthcare Voicebot! Stay healthy!

