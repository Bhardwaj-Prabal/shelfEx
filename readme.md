# Smart Flashcard Generator

![Flashcard Generator Screenshot](/home/lghoda69/Desktop/shelf/shelfEx/assets/1.png)
![Flashcard Generator Screenshot](/home/lghoda69/Desktop/shelf/shelfEx/assets/2.png)

A web application that transforms educational content into beautiful, interactive flashcards using AI.

## Features ✨

- **Multiple Input Options**:
  - 📝 Direct text input
  - 📂 File upload (PDF/TXT)
  
- **Customizable Generation**:
  - 🔢 Adjust number of flashcards (5-30)
  - 🎚️ Set difficulty level (Easy/Medium/Hard)
  - ✏️ Control answer length (Short/Medium/Long)

- **Interactive Flashcards**:
  - 🃏 Flip animation to reveal answers
  - 🗂️ Organized by content sections
  - 🔍 Filter by sections

- **Export Options**:
  - 📊 JSON format
  - 📈 CSV format
  - 🗃️ Anki-compatible format

## Tech Stack 💻

**Frontend**:
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Animate.css

**Backend**:
- Python Flask
- Google Generative AI API
- PyPDF2 (for PDF processing)

## Installation 🛠️ 

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flashcard-generator.git
cd flashcard-generator
```
2. Set up enviornment :
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3.Install dependencies:
```bash
pip install -r requirements.txt
```
4.Set your API key:
```bash
export YOUR_API_KEY="your_google_api_key_here"
```
5.Run the application:
```bash
python app.py
```