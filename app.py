from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PyPDF2 import PdfReader
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=API_KEY)

def extract_text_from_file(file):
    """Extract text with structure from uploaded file"""
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.filename.endswith('.pdf'):
        text = ""
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    return ""

def detect_structure(text):
    """Identify headings and sections in text"""
    sections = []
    current_section = {"title": "Main Content", "content": ""}
    
    for line in text.split('\n'):
        if re.match(r'^(#+ |Chapter \d+|Section \d+\.)', line.strip()):
            if current_section["content"]:
                sections.append(current_section)
            current_section = {"title": line.strip(), "content": ""}
        else:
            current_section["content"] += line + "\n"
    
    if current_section["content"]:
        sections.append(current_section)
    
    return sections if len(sections) > 1 else [{"title": "All Content", "content": text}]

def generate_flashcards(text, subject=None, num_flashcards=10, difficulty="medium", answer_size="medium"):
    """Generate flashcards with specified parameters"""
    difficulty_prompt = {
        "easy": "Create simple questions about basic facts and definitions.",
        "medium": "Include both factual and conceptual questions.",
        "hard": "Generate challenging questions that require analysis and critical thinking."
    }.get(difficulty, "")
    
    answer_size_prompt = {
        "short": "Provide concise answers (1 sentence maximum).",
        "medium": "Provide detailed answers (2-3 sentences).",
        "long": "Provide comprehensive answers (paragraph length)."
    }.get(answer_size, "")
    
    prompt = f"""
    Generate {num_flashcards} high-quality flashcards from this content.
    Format each as: Q: [question] | A: [answer]
    {f"Subject: {subject}" if subject else ""}
    {difficulty_prompt}
    {answer_size_prompt}
    
    Preserve any section headings from the original content.
    
    Content:
    {text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(prompt)
        return parse_flashcards(response.text)
    except Exception as e:
        return {"error": str(e)}

def parse_flashcards(text):
    """Parse generated flashcards with structure"""
    flashcards = []
    current_section = "General"
    
    for line in text.split('\n'):
        if line.startswith('#'):
            current_section = line.strip('#').strip()
        elif '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                card = {
                    "question": parts[0].replace('Q:', '').strip(),
                    "answer": parts[1].replace('A:', '').strip(),
                    "section": current_section
                }
                flashcards.append(card)
    
    return flashcards

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    input_method = request.form.get('input_method')
    subject = request.form.get('subject')
    num_flashcards = int(request.form.get('num_flashcards', 10))
    difficulty = request.form.get('difficulty', 'medium')
    answer_size = request.form.get('answer_size', 'medium')
    
    if input_method == 'text':
        text = request.form.get('text', '')
    else:
        file = request.files.get('file')
        text = extract_text_from_file(file) if file else ''
    
    if not text:
        return jsonify({"error": "No content provided"})
    
    structured_content = detect_structure(text)
    flashcards = []
    for section in structured_content:
        result = generate_flashcards(
            section["content"],
            subject,
            max(3, num_flashcards // len(structured_content)),
            difficulty,
            answer_size
        )
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result)
        flashcards.extend(result)
    
    return jsonify({
        "flashcards": flashcards,
        "sections": [s["title"] for s in structured_content]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
