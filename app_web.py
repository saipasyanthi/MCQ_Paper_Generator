#!/usr/bin/env python3
"""
Web-based MCQ Paper Generator
Run this to launch the web application accessible on tablets/phones
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import secrets
from pathlib import Path

from pdf_extractor import PDFQuestionExtractor
from document_generator import QuestionPaperGenerator, AnswerKeyGenerator
from database import QuestionDatabase
from license_manager import LicenseValidator

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize database
db = QuestionDatabase()

# License check
def check_license():
    """Check if valid license exists."""
    is_valid, message, license_data = LicenseValidator.validate()
    return is_valid, message

@app.before_request
def verify_license():
    """Verify license before each request."""
    if request.endpoint and request.endpoint != 'static' and not request.endpoint.startswith('license'):
        is_valid, message = check_license()
        if not is_valid:
            return render_template('license_error.html', message=message), 403

@app.route('/')
def index():
    """Main page."""
    is_valid, license_msg = check_license()
    stats = {
        'total_questions': len(db.get_all_questions()),
        'subjects': len(set(q['subject'] for q in db.get_all_questions())),
        'license_message': license_msg
    }
    return render_template('index.html', stats=stats)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload and extract questions from PDF."""
    if request.method == 'GET':
        return render_template('upload.html')
    
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract questions
        subject = request.form.get('subject', 'General')
        chapter = request.form.get('chapter', 'Chapter 1')
        
        extractor = PDFQuestionExtractor()
        questions = extractor.extract_from_pdf(filepath)
        
        # Add to database
        added_count = 0
        for q in questions:
            q['subject'] = subject
            q['chapter'] = chapter
            db.add_question(q)
            added_count += 1
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': f'Successfully extracted and added {added_count} questions',
            'count': added_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/questions')
def questions():
    """View all questions."""
    all_questions = db.get_all_questions()
    subjects = sorted(set(q['subject'] for q in all_questions))
    return render_template('questions.html', questions=all_questions, subjects=subjects)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """Add a single question manually."""
    if request.method == 'GET':
        return render_template('add_question.html')
    
    try:
        question_data = {
            'question': request.form.get('question'),
            'options': [
                request.form.get('option1'),
                request.form.get('option2'),
                request.form.get('option3'),
                request.form.get('option4')
            ],
            'correct_answer': int(request.form.get('correct_answer')),
            'subject': request.form.get('subject', 'General'),
            'chapter': request.form.get('chapter', 'Chapter 1'),
            'difficulty': request.form.get('difficulty', 'Medium')
        }
        
        question_id = db.add_question(question_data)
        
        return jsonify({
            'success': True,
            'message': 'Question added successfully',
            'question_id': question_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate MCQ paper."""
    if request.method == 'GET':
        all_questions = db.get_all_questions()
        subjects = sorted(set(q['subject'] for q in all_questions))
        return render_template('generate.html', subjects=subjects)
    
    try:
        # Get form data
        college_name = request.form.get('college_name')
        exam_name = request.form.get('exam_name')
        exam_date = request.form.get('exam_date')
        num_questions = int(request.form.get('num_questions', 20))
        subject = request.form.get('subject', '')
        
        # Get questions
        if subject and subject != 'All':
            available = db.get_questions_by_subject(subject)
        else:
            available = db.get_all_questions()
        
        if len(available) < num_questions:
            return jsonify({
                'error': f'Not enough questions. Available: {len(available)}, Requested: {num_questions}'
            }), 400
        
        # Select random questions
        import random
        selected = random.sample(available, num_questions)
        selected_dict = {i+1: q for i, q in enumerate(selected)}
        
        # Generate question paper
        generator = QuestionPaperGenerator(college_name, exam_name, exam_date, selected_dict)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        question_paper = f"question_paper_{timestamp}.docx"
        question_path = os.path.join(app.config['OUTPUT_FOLDER'], question_paper)
        generator.generate(question_path)
        
        # Generate answer key
        answer_gen = AnswerKeyGenerator(college_name, exam_name, exam_date, selected_dict)
        answer_key = f"answer_key_{timestamp}.docx"
        answer_path = os.path.join(app.config['OUTPUT_FOLDER'], answer_key)
        answer_gen.generate(answer_path)
        
        return jsonify({
            'success': True,
            'message': 'Papers generated successfully',
            'question_paper': question_paper,
            'answer_key': answer_key
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    """Download generated file."""
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

@app.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    """Delete a question."""
    try:
        db.delete_question(question_id)
        return jsonify({'success': True, 'message': 'Question deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    """Show statistics."""
    all_questions = db.get_all_questions()
    subjects = {}
    difficulties = {'Easy': 0, 'Medium': 0, 'Hard': 0}
    
    for q in all_questions:
        subject = q.get('subject', 'General')
        subjects[subject] = subjects.get(subject, 0) + 1
        diff = q.get('difficulty', 'Medium')
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    return render_template('stats.html', 
                         total=len(all_questions),
                         subjects=subjects,
                         difficulties=difficulties)

if __name__ == '__main__':
    # Get local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*60)
    print("MCQ PAPER GENERATOR - WEB APPLICATION")
    print("="*60)
    print(f"\nStarting server...")
    print(f"\nAccess from this computer: http://localhost:8080")
    print(f"Access from tablet/phone: http://{local_ip}:8080")
    print(f"\nMake sure your tablet/phone is on the same WiFi network!")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Run server accessible from network
    app.run(host='0.0.0.0', port=8080, debug=False)
