"""
PDF Question Extractor
Extracts questions from PDF files
"""

import pdfplumber
from pathlib import Path
import re


class PDFQuestionExtractor:
    """Extract questions from PDF files."""
    
    def __init__(self, pdf_path):
        """Initialize extractor with PDF file.
        
        Args:
            pdf_path: Path to PDF file
        """
        self.pdf_path = pdf_path
        self.text = ""
        self.pages_text = []
    
    def extract_text(self):
        """Extract all text from PDF.
        
        Returns:
            Dictionary with page-wise text
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    self.pages_text.append({
                        "page": page_num,
                        "text": page_text
                    })
                    self.text += page_text + "\n"
            
            return True, "Text extracted successfully"
        except Exception as e:
            return False, f"Error extracting text: {str(e)}"
    
    def extract_questions(self):
        """Extract questions from PDF text.
        
        Returns:
            Tuple (success, questions_dict, message)
            questions_dict format: {id: {question, options, correct_answer, explanation}}
        """
        if not self.text:
            success, msg = self.extract_text()
            if not success:
                return False, {}, msg
        
        questions = {}
        question_id = 1
        
        # Try multiple question patterns
        patterns = [
            # Pattern 1: Q1. Question text\nA) option\nB) option\nC) option\nD) option\nAnswer: B
            r'Q\.?\s*(\d+)[.\):\s]+([^A-D\n]+)\n([A-D]\)[^\n]+\n)+.*?Answer[:\s]+([A-D])',
            
            # Pattern 2: 1. Question text\nA) option\nB) option\nC) option\nD) option
            r'(\d+)[.\):\s]+([^A-D\n]+)\n([A-D]\)[^\n]+(?:\n[A-D]\)[^\n]+){2,3})',
            
            # Pattern 3: Question. text\nA. option\nB. option\nC. option\nD. option
            r'([A-D])\.\s+([^A-D\n]+(?:\n(?![A-D]\.).*)*)',
        ]
        
        # Split by question markers
        lines = self.text.split('\n')
        current_question = None
        current_options = {}
        current_answer = None
        current_explanation = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for question start (Q1., 1., Question:, etc.)
            question_match = re.match(r'^(?:Q\.?\s*)?(\d+)[.\):\s]+(.+)', line)
            if question_match and current_question is not None:
                # Save previous question
                if current_options:
                    questions[question_id] = {
                        "question": current_question,
                        "options": current_options,
                        "correct_answer": current_answer or "A",
                        "explanation": current_explanation.strip() or "No explanation provided"
                    }
                    question_id += 1
                
                # Start new question
                current_question = question_match.group(2)
                current_options = {}
                current_answer = None
                current_explanation = ""
            
            elif question_match and current_question is None:
                current_question = question_match.group(2)
                current_options = {}
                current_answer = None
                current_explanation = ""
            
            # Check for options (A), B), C), D) or A. B. C. D.
            elif re.match(r'^[A-D][.\)]\s+', line):
                option_match = re.match(r'^([A-D])[.\)]\s+(.+)', line)
                if option_match:
                    option_key = option_match.group(1)
                    option_text = option_match.group(2)
                    current_options[option_key] = option_text
            
            # Check for answer indicator
            elif re.match(r'^(?:Answer|Correct|Solution)[:\s]+([A-D])', line, re.IGNORECASE):
                ans_match = re.match(r'^(?:Answer|Correct|Solution)[:\s]+([A-D])', line, re.IGNORECASE)
                current_answer = ans_match.group(1)
            
            # Check for explanation
            elif re.match(r'^(?:Explanation|Solution|Note|Reason)[:\s]+', line, re.IGNORECASE):
                current_explanation = line
        
        # Save last question
        if current_question and current_options:
            questions[question_id] = {
                "question": current_question,
                "options": current_options,
                "correct_answer": current_answer or "A",
                "explanation": current_explanation.strip() or "No explanation provided"
            }
        
        if not questions:
            # Fallback: try to extract any text with options
            questions = self._fallback_extraction()
        
        if questions:
            return True, questions, f"Extracted {len(questions)} questions"
        else:
            return False, {}, "No questions found in PDF"
    
    def _fallback_extraction(self):
        """Fallback method to extract questions."""
        questions = {}
        question_id = 1
        
        # Split text into potential questions
        text_blocks = re.split(r'\n\s*\n+', self.text)
        
        for block in text_blocks:
            if len(block) < 10:  # Skip very short blocks
                continue
            
            lines = block.split('\n')
            if len(lines) < 5:  # Need at least question + 4 options
                continue
            
            # First line is question
            question_text = lines[0].strip()
            if question_text.startswith(('Q', '1', 'A')):
                question_text = re.sub(r'^[Q1A\d\.\):\s]+', '', question_text).strip()
            
            # Next 4 lines are options
            options = {}
            option_idx = 0
            for line in lines[1:]:
                if option_idx >= 4:
                    break
                line = line.strip()
                if line and not re.match(r'^Answer|Solution|Correct', line, re.IGNORECASE):
                    # Remove option markers
                    clean_line = re.sub(r'^[A-D][.\)]\s+', '', line)
                    if clean_line:
                        options[['A', 'B', 'C', 'D'][option_idx]] = clean_line
                        option_idx += 1
            
            if len(options) == 4:
                questions[question_id] = {
                    "question": question_text,
                    "options": options,
                    "correct_answer": "A",  # Default
                    "explanation": "See PDF for explanation"
                }
                question_id += 1
        
        return questions
    
    def get_summary(self):
        """Get extraction summary."""
        return {
            "total_pages": len(self.pages_text),
            "total_text_length": len(self.text),
            "file_path": str(self.pdf_path)
        }


class QuestionValidator:
    """Validate extracted questions."""
    
    @staticmethod
    def validate_question(question_data):
        """Validate a single question.
        
        Args:
            question_data: Dictionary with question info
            
        Returns:
            Tuple (is_valid, errors)
        """
        errors = []
        
        # Check question text
        if not question_data.get("question") or len(question_data.get("question", "")) < 5:
            errors.append("Question text too short or missing")
        
        # Check options
        options = question_data.get("options", {})
        if len(options) != 4:
            errors.append(f"Expected 4 options, got {len(options)}")
        
        required_options = {'A', 'B', 'C', 'D'}
        if set(options.keys()) != required_options:
            errors.append(f"Options must be A, B, C, D. Got: {list(options.keys())}")
        
        # Check each option
        for key, value in options.items():
            if not value or len(str(value)) < 2:
                errors.append(f"Option {key} is too short or empty")
        
        # Check correct answer
        correct_answer = question_data.get("correct_answer", "")
        if correct_answer not in required_options:
            errors.append(f"Correct answer must be A-D, got {correct_answer}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_questions(questions_dict):
        """Validate all questions.
        
        Args:
            questions_dict: Dictionary of questions
            
        Returns:
            Tuple (is_valid, validation_report)
        """
        report = {
            "total": len(questions_dict),
            "valid": 0,
            "invalid": 0,
            "errors": {}
        }
        
        for qid, question in questions_dict.items():
            is_valid, errors = QuestionValidator.validate_question(question)
            if is_valid:
                report["valid"] += 1
            else:
                report["invalid"] += 1
                report["errors"][qid] = errors
        
        return report["invalid"] == 0, report


def extract_pdf_questions(pdf_path):
    """Convenience function to extract questions from PDF.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Tuple (success, questions_dict, message)
    """
    extractor = PDFQuestionExtractor(pdf_path)
    success, msg = extractor.extract_text()
    
    if not success:
        return False, {}, msg
    
    success, questions, msg = extractor.extract_questions()
    
    if success:
        # Validate questions
        is_valid, report = QuestionValidator.validate_questions(questions)
        if not is_valid:
            msg += f" ({report['valid']} valid, {report['invalid']} need verification)"
    
    return success, questions, msg
