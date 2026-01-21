#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the MCQ Generator
without using the interactive CLI.
"""

from database import get_questions
from document_generator import QuestionPaperGenerator, AnswerKeyGenerator
from pdf_converter import PDFConverter
import os
from datetime import datetime


def generate_sample_papers():
    """Generate sample question papers programmatically."""
    
    # Configuration
    college_name = "ABC University"
    exam_name = "Physics - Midterm Exam"
    exam_date = "20-01-2026"
    question_ids = [1, 3, 5, 7, 9]
    
    # Output directory
    output_dir = "output/sample_run"
    os.makedirs(output_dir, exist_ok=True)
    
    # Fetch questions
    questions = get_questions(question_ids)
    print(f"Generated papers for {len(questions)} questions")
    
    # Generate Question Paper
    print("\n[1] Generating Question Paper...")
    qp_filename = f"{output_dir}/Question_Paper_Sample.docx"
    qp_gen = QuestionPaperGenerator(college_name, exam_name, exam_date, questions)
    qp_gen.generate(qp_filename)
    print(f"✓ Created: {qp_filename}")
    
    # Generate Answer Key
    print("[2] Generating Answer Key & Solutions...")
    ak_filename = f"{output_dir}/Answer_Key_Solutions_Sample.docx"
    ak_gen = AnswerKeyGenerator(college_name, exam_name, exam_date, questions)
    ak_gen.generate(ak_filename)
    print(f"✓ Created: {ak_filename}")
    
    # Convert to PDF
    print("[3] Converting to PDF...")
    pdf_result = PDFConverter.convert_documents(qp_filename, ak_filename, output_dir)
    
    if pdf_result:
        qp_pdf, ak_pdf = pdf_result
        print(f"✓ PDF created: {qp_pdf}")
        print(f"✓ PDF created: {ak_pdf}")
    else:
        print("⚠ PDF conversion skipped (LibreOffice not installed)")
    
    print(f"\n✓ All files saved in: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    generate_sample_papers()
