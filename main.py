#!/usr/bin/env python3
"""
MCQ Question Paper Generator
Generates Question Paper and Answer Key in Word and PDF formats.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

from database import get_questions, validate_question_ids, get_available_question_ids
from document_generator import QuestionPaperGenerator, AnswerKeyGenerator
from pdf_converter import PDFConverter


class MCQPaperGenerator:
    """Main application for generating MCQ papers."""
    
    def __init__(self):
        self.output_dir = "output"
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def parse_question_input(self, question_input):
        """Parse comma-separated question numbers into a list.
        
        Args:
            question_input: String like "1,3,5,7" or "1, 3, 5, 7"
            
        Returns:
            List of integers representing question IDs
        """
        try:
            question_ids = [int(q.strip()) for q in question_input.split(',')]
            return question_ids
        except ValueError:
            print("Error: Please enter question numbers separated by commas (e.g., 1,3,5,7)")
            return None
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "="*60)
        print("        MCQ PAPER GENERATOR")
        print("="*60)
        print("\nOptions:")
        print("1. Generate Question Paper and Answer Key")
        print("2. View Available Questions")
        print("3. Exit")
        print("-"*60)
    
    def display_available_questions(self):
        """Display all available questions."""
        available_ids = get_available_question_ids()
        print("\nAvailable Questions:")
        print("-"*60)
        for qid in available_ids:
            from database import QUESTIONS_DATABASE
            q = QUESTIONS_DATABASE[qid]
            print(f"Q{qid}: {q['question']}")
        print("-"*60)
    
    def generate_papers(self):
        """Generate question paper and answer key."""
        print("\n" + "-"*60)
        print("QUESTION PAPER GENERATION")
        print("-"*60)
        
        # Get college name
        college_name = input("\nEnter College Name: ").strip()
        if not college_name:
            print("Error: College name cannot be empty!")
            return
        
        # Get exam name
        exam_name = input("Enter Exam Name (e.g., 'Midterm Exam', 'Final Test'): ").strip()
        if not exam_name:
            print("Error: Exam name cannot be empty!")
            return
        
        # Get date
        date = input("Enter Exam Date (e.g., '15-01-2026' or press Enter for today): ").strip()
        if not date:
            date = datetime.now().strftime("%d-%m-%Y")
        
        # Get question numbers
        available_ids = get_available_question_ids()
        print(f"\nAvailable question IDs: {', '.join(map(str, available_ids))}")
        question_input = input("Enter question numbers separated by commas (e.g., 1,3,5,7): ").strip()
        
        if not question_input:
            print("Error: Please enter at least one question number!")
            return
        
        question_ids = self.parse_question_input(question_input)
        if question_ids is None:
            return
        
        # Validate question IDs
        is_valid, invalid_ids, valid_ids = validate_question_ids(question_ids)
        
        if invalid_ids:
            print(f"\nWarning: Question IDs {invalid_ids} do not exist in the database.")
        
        if not valid_ids:
            print("Error: No valid question IDs provided!")
            return
        
        print(f"\nSelected questions: {valid_ids}")
        
        # Fetch questions
        questions = get_questions(valid_ids)
        
        # Generate timestamps for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate Question Paper
        print("\n" + "-"*60)
        print("Generating Question Paper...")
        
        question_paper_filename = f"Question_Paper_{timestamp}.docx"
        question_paper_path = os.path.join(self.output_dir, question_paper_filename)
        
        qp_gen = QuestionPaperGenerator(college_name, exam_name, date, questions)
        qp_gen.generate(question_paper_path)
        print(f"✓ Question Paper (DOCX) created: {question_paper_path}")
        
        # Generate Answer Key
        print("\nGenerating Answer Key & Solutions...")
        
        answer_key_filename = f"Answer_Key_Solutions_{timestamp}.docx"
        answer_key_path = os.path.join(self.output_dir, answer_key_filename)
        
        ak_gen = AnswerKeyGenerator(college_name, exam_name, date, questions)
        ak_gen.generate(answer_key_path)
        print(f"✓ Answer Key (DOCX) created: {answer_key_path}")
        
        # Convert to PDF
        print("\n" + "-"*60)
        print("Converting to PDF format...")
        
        pdf_result = PDFConverter.convert_documents(
            question_paper_path,
            answer_key_path,
            self.output_dir
        )
        
        if pdf_result:
            qp_pdf, ak_pdf = pdf_result
            print("\n" + "="*60)
            print("✓ ALL DOCUMENTS GENERATED SUCCESSFULLY!")
            print("="*60)
            print(f"\nQuestion Paper (DOCX): {question_paper_path}")
            print(f"Question Paper (PDF):  {qp_pdf}")
            print(f"\nAnswer Key (DOCX): {answer_key_path}")
            print(f"Answer Key (PDF):  {ak_pdf}")
            print(f"\nAll files saved in: {os.path.abspath(self.output_dir)}")
        else:
            print("\n⚠ Documents generated in DOCX format only.")
            print("(PDF conversion requires LibreOffice)")
            print(f"\nQuestion Paper: {question_paper_path}")
            print(f"Answer Key: {answer_key_path}")
    
    def run(self):
        """Run the application."""
        while True:
            self.display_menu()
            choice = input("Select an option (1-3): ").strip()
            
            if choice == '1':
                self.generate_papers()
            elif choice == '2':
                self.display_available_questions()
            elif choice == '3':
                print("\nThank you for using MCQ Paper Generator!")
                sys.exit(0)
            else:
                print("Invalid choice! Please select 1, 2, or 3.")


def main():
    """Main entry point."""
    try:
        app = MCQPaperGenerator()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
