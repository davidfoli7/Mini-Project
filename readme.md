# AI Personalized Learning Platform

A modern, interactive learning platform featuring multiple study modes including flashcards, multiple-choice questions, case studies, and text summarization.

## Features

- **General Q&A**: Get detailed answers to any question
- **Interactive Flashcards**: Study with dynamic, flippable cards
- **Multiple Choice Questions**: Test your knowledge with MCQs
- **Case Studies**: Learn from detailed case analyses
- **Text Summarization**: Get concise summaries of long texts
- **Voice Input**: Supports voice-to-text for easy input
- **Progress Tracking**: Monitor your learning progress

## Prerequisites

- Python 3.8 or higher
- Node.js 14.x or higher (optional, for development)
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Dependencies

### Python Dependencies
```bash
Flask==2.0.1
requests==2.26.0
flask-cors==3.0.10
SpeechRecognition==3.8.1
gTTS==2.3.1
pyaudio==0.2.11
```

### Frontend Dependencies (automatically loaded via CDN)
- Tailwind CSS
- Font Awesome
- jQuery
- Google Fonts (Poppins)

## Installation

1. Download or clone this repository to your local machine
2. Navigate to the project directory:
```bash
cd AI_Personalized_Learning
```

3. Create a virtual environment:
```bash
python -m venv venv
```

4. Activate the virtual environment:

On Windows:
```bash
.\venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

5. Install Python dependencies:
```bash
pip install -r requirements.txt
```

6. Set up environment variables:
Create a `.env` file in the root directory and add:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running the Application

### **Important Note: Folder Structure**
- **`backend/`** folder contains the **Frontend web server** (Node.js/Express)
- **`ai_service/`** folder contains the **Backend AI server** (Python/Flask)

### **Step 1: Start the Frontend Server (Web Interface)**
```bash
cd backend
npm install
node server.js
```
**Access at:** http://localhost:3001

### **Step 2: Start the Backend AI Service**
```bash
cd ai_service
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python app.py
```
**Runs on:** http://localhost:3002

## Project Structure

```
AI_Personalized_Learning/
├── backend/              # Frontend web server (Node.js/Express)
│   ├── server.js         # Express server (Port 3001)
│   ├── templates/        # HTML files
│   │   └── index.html    # Main web interface
│   ├── static/           # CSS, JS, images
│   │   ├── script.js     # Frontend JavaScript
│   │   ├── styles.css    # Main styles
│   │   └── images/       # Logo and assets
│   ├── controllers/      # Business logic
│   ├── models/          # Data models
│   └── routes/          # API routes
├── ai_service/           # Backend AI server (Python/Flask)
│   ├── app.py           # Flask AI server (Port 3002)
│   ├── requirements.txt # Python dependencies
│   └── venv/           # Virtual environment
├── package.json         # Project metadata
└── readme.md           # This documentation
```

## Usage

1. Select a learning mode from the sidebar:
   - General Q&A
   - Flashcards
   - Multiple Choice
   - Case Studies
   - Summarization

2. Enter your query or topic in the input field
3. For Flashcards/MCQs/Case Studies:
   - Use the number selector to choose how many items to generate
   - Click through the cards/questions
   - Track your progress in the sidebar

## API Keys

This application uses the Google Gemini API. You'll need to:
1. Get an API key from Google AI Studio
2. Add it to your `.env` file
3. Never commit your API key to version control

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

Voice input functionality is currently supported only in Chrome and Edge.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for AI capabilities
- Tailwind CSS for styling
- Font Awesome for icons
- jQuery for DOM manipulation

## Running Instructions

### **Frontend Server (Web Interface):**
1. Go to the `backend` directory
2. Run: `node server.js`
3. Visit: http://localhost:3001

### **Backend AI Service:**
1. Navigate to the `ai_service` directory
2. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Run: `python app.py`
4. Service runs on: http://localhost:3002


