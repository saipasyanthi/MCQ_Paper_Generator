# Database of MCQ Questions
# Each question contains: id, question text, options (A, B, C, D), correct answer, explanation/solution

import json
from pathlib import Path


class QuestionDatabase:
    """Manage MCQ questions database."""
    
    def __init__(self, db_file="questions_db.json"):
        self.db_file = Path(db_file)
        self.questions = {}
        self.next_id = 1
        self.load()
    
    def load(self):
        """Load questions from file."""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.questions = {int(k): v for k, v in data.get('questions', {}).items()}
                    self.next_id = data.get('next_id', 1)
            except:
                pass
        
        # If no questions, load defaults
        if not self.questions:
            self.questions = STATIC_QUESTIONS.copy()
            self.next_id = max(self.questions.keys()) + 1 if self.questions else 1
            self.save()
    
    def save(self):
        """Save questions to file."""
        data = {
            'questions': {str(k): v for k, v in self.questions.items()},
            'next_id': self.next_id
        }
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_question(self, question_data):
        """Add a new question."""
        question_id = self.next_id
        self.questions[question_id] = {
            'id': question_id,
            'question': question_data['question'],
            'options': question_data['options'],
            'correct_answer': question_data['correct_answer'],
            'subject': question_data.get('subject', 'General'),
            'chapter': question_data.get('chapter', 'Chapter 1'),
            'difficulty': question_data.get('difficulty', 'Medium')
        }
        self.next_id += 1
        self.save()
        return question_id
    
    def get_question(self, question_id):
        """Get a single question."""
        return self.questions.get(question_id)
    
    def get_all_questions(self):
        """Get all questions as a list."""
        return list(self.questions.values())
    
    def get_questions_by_subject(self, subject):
        """Get questions for a specific subject."""
        return [q for q in self.questions.values() if q.get('subject') == subject]
    
    def delete_question(self, question_id):
        """Delete a question."""
        if question_id in self.questions:
            del self.questions[question_id]
            self.save()
            return True
        return False
    
    def update_question(self, question_id, question_data):
        """Update an existing question."""
        if question_id in self.questions:
            self.questions[question_id].update(question_data)
            self.save()
            return True
        return False


STATIC_QUESTIONS = {
    1: {
        "question": "What is the capital of France?",
        "options": {
            "A": "London",
            "B": "Paris",
            "C": "Berlin",
            "D": "Madrid"
        },
        "correct_answer": "B",
        "explanation": "Paris is the capital and most populous city of France, located in the north-central part of the country on the Seine River."
    },
    2: {
        "question": "Which planet is known as the Red Planet?",
        "options": {
            "A": "Venus",
            "B": "Jupiter",
            "C": "Mars",
            "D": "Saturn"
        },
        "correct_answer": "C",
        "explanation": "Mars is often called the Red Planet due to its reddish appearance caused by iron oxide (rust) on its surface."
    },
    3: {
        "question": "What is the chemical symbol for Gold?",
        "options": {
            "A": "Go",
            "B": "Gd",
            "C": "Au",
            "D": "Ag"
        },
        "correct_answer": "C",
        "explanation": "The chemical symbol for Gold is Au, derived from its Latin name 'Aurum'."
    },
    4: {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": {
            "A": "Christopher Marlowe",
            "B": "William Shakespeare",
            "C": "Ben Jonson",
            "D": "John Webster"
        },
        "correct_answer": "B",
        "explanation": "William Shakespeare wrote 'Romeo and Juliet', one of his most famous tragedies, likely written between 1594 and 1596."
    },
    5: {
        "question": "What is the largest ocean on Earth?",
        "options": {
            "A": "Atlantic Ocean",
            "B": "Indian Ocean",
            "C": "Arctic Ocean",
            "D": "Pacific Ocean"
        },
        "correct_answer": "D",
        "explanation": "The Pacific Ocean is the largest ocean on Earth, covering approximately 165 million square kilometers."
    },
    6: {
        "question": "Which element has the atomic number 6?",
        "options": {
            "A": "Nitrogen",
            "B": "Oxygen",
            "C": "Carbon",
            "D": "Boron"
        },
        "correct_answer": "C",
        "explanation": "Carbon has atomic number 6, meaning it has 6 protons in its nucleus. It's the basis for all organic compounds."
    },
    7: {
        "question": "In which year did the Titanic sink?",
        "options": {
            "A": "1912",
            "B": "1915",
            "C": "1920",
            "D": "1925"
        },
        "correct_answer": "A",
        "explanation": "The RMS Titanic sank on April 15, 1912, after colliding with an iceberg during its maiden voyage."
    },
    8: {
        "question": "What is the smallest prime number?",
        "options": {
            "A": "1",
            "B": "2",
            "C": "3",
            "D": "5"
        },
        "correct_answer": "B",
        "explanation": "The smallest prime number is 2. It is the only even prime number and the only prime that is not odd."
    },
    9: {
        "question": "Which country is home to the Great Wall?",
        "options": {
            "A": "Japan",
            "B": "India",
            "C": "China",
            "D": "Vietnam"
        },
        "correct_answer": "C",
        "explanation": "The Great Wall of China is one of the most impressive architectural feats, built over several centuries to protect Chinese states."
    },
    10: {
        "question": "What is the powerhouse of the cell?",
        "options": {
            "A": "Nucleus",
            "B": "Mitochondria",
            "C": "Ribosome",
            "D": "Golgi apparatus"
        },
        "correct_answer": "B",
        "explanation": "Mitochondria is known as the powerhouse of the cell because it is responsible for producing energy (ATP) through cellular respiration."
    }
}

# Legacy database reference
QUESTIONS_DATABASE = STATIC_QUESTIONS


def get_question(question_id):
    """Retrieve a single question from the database."""
    return STATIC_QUESTIONS.get(question_id)


def get_questions(question_ids):
    """Retrieve multiple questions from the database.
    
    Args:
        question_ids: List of question IDs to fetch
        
    Returns:
        Dictionary with question IDs as keys and question data as values
    """
    questions = {}
    for qid in question_ids:
        if qid in STATIC_QUESTIONS:
            questions[qid] = STATIC_QUESTIONS[qid]
    return questions


def get_all_questions():
    """Retrieve all questions from the database."""
    return STATIC_QUESTIONS


def get_available_question_ids():
    """Get list of all available question IDs."""
    return sorted(list(STATIC_QUESTIONS.keys()))


def validate_question_ids(question_ids):
    """Validate if all question IDs exist in the database.
    
    Args:
        question_ids: List of question IDs to validate
        
    Returns:
        Tuple (is_valid, invalid_ids, valid_ids)
    """
    available = set(STATIC_QUESTIONS.keys())
    provided = set(question_ids)
    invalid = provided - available
    valid = provided & available
    
    return len(invalid) == 0, list(invalid), sorted(list(valid))
