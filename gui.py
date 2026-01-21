"""
PyQt5 GUI for MCQ Paper Generator - PDF Edition
Desktop application with PDF loading and random question selection
"""

import sys
import os
import random
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QScrollArea, QMessageBox,
    QFileDialog, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from pdf_extractor import extract_pdf_questions
from document_generator import QuestionPaperGenerator, AnswerKeyGenerator
from pdf_converter import PDFConverter
from license_manager import LicenseValidator


class DocumentGeneratorThread(QThread):
    """Worker thread for document generation."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, college_name, exam_name, exam_date, questions, output_dir):
        super().__init__()
        self.college_name = college_name
        self.exam_name = exam_name
        self.exam_date = exam_date
        self.questions = questions
        self.output_dir = output_dir
    
    def run(self):
        try:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate Question Paper
            self.progress.emit("Generating Question Paper...")
            qp_filename = f"Question_Paper_{timestamp}.docx"
            qp_path = os.path.join(self.output_dir, qp_filename)
            qp_gen = QuestionPaperGenerator(self.college_name, self.exam_name, self.exam_date, self.questions)
            qp_gen.generate(qp_path)
            
            # Generate Answer Key
            self.progress.emit("Generating Answer Key & Solutions...")
            ak_filename = f"Answer_Key_Solutions_{timestamp}.docx"
            ak_path = os.path.join(self.output_dir, ak_filename)
            ak_gen = AnswerKeyGenerator(self.college_name, self.exam_name, self.exam_date, self.questions)
            ak_gen.generate(ak_path)
            
            # Convert to PDF
            self.progress.emit("Converting to PDF format...")
            pdf_result = PDFConverter.convert_documents(qp_path, ak_path, self.output_dir)
            
            if pdf_result:
                self.progress.emit("✓ All documents generated successfully!")
                self.finished.emit(True, f"Documents saved to:\n{os.path.abspath(self.output_dir)}")
            else:
                self.progress.emit("✓ Documents generated (PDF conversion skipped)")
                self.finished.emit(True, f"DOCX files saved to:\n{os.path.abspath(self.output_dir)}")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class PDFLoaderThread(QThread):
    """Worker thread for PDF loading."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, dict, str)
    
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
    
    def run(self):
        try:
            self.progress.emit(f"Loading PDF: {Path(self.pdf_path).name}")
            success, questions, message = extract_pdf_questions(self.pdf_path)
            
            if success:
                self.progress.emit(f"✓ Loaded {len(questions)} questions")
                self.finished.emit(True, questions, message)
            else:
                self.finished.emit(False, {}, message)
        except Exception as e:
            self.finished.emit(False, {}, f"Error loading PDF: {str(e)}")


class MCQPaperGeneratorGUI(QMainWindow):
    """Main GUI application window with PDF loading."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCQ Paper Generator - PDF Edition")
        self.setGeometry(100, 100, 1300, 850)
        
        self.loaded_questions = {}
        self.selected_questions = {}
        self.pdf_path = None
        self.generator_thread = None
        self.loader_thread = None
        
        # Check license
        if not self.check_license():
            sys.exit(1)
        
        self.init_ui()
    
    def check_license(self):
        """Check if valid license exists."""
        is_valid, message, license_data = LicenseValidator.validate()
        
        if not is_valid:
            QMessageBox.critical(
                self,
                "License Required",
                "Valid license is required to use this application.\n\n" + message
            )
            return False
        
        return True
    
    def init_ui(self):
        """Initialize the user interface."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        
        # ===== LEFT PANEL - Input Fields =====
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Title
        title = QLabel("MCQ Paper Generator")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        left_layout.addWidget(title)
        
        left_layout.addWidget(QLabel(""))
        
        # PDF Loading Section
        left_layout.addWidget(QLabel("📄 Load PDF:"))
        pdf_btn_layout = QHBoxLayout()
        
        self.pdf_label = QLabel("No PDF loaded")
        self.pdf_label.setStyleSheet("color: gray;")
        pdf_btn_layout.addWidget(self.pdf_label)
        
        load_pdf_btn = QPushButton("Load PDF")
        load_pdf_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        load_pdf_btn.clicked.connect(self.load_pdf)
        pdf_btn_layout.addWidget(load_pdf_btn)
        
        left_layout.addLayout(pdf_btn_layout)
        
        left_layout.addWidget(QLabel(""))
        
        # College Name
        left_layout.addWidget(QLabel("College Name:"))
        self.college_input = QLineEdit()
        self.college_input.setPlaceholderText("e.g., ABC University")
        left_layout.addWidget(self.college_input)
        
        left_layout.addWidget(QLabel(""))
        
        # Exam Name
        left_layout.addWidget(QLabel("Exam Name:"))
        self.exam_input = QLineEdit()
        self.exam_input.setPlaceholderText("e.g., Physics - Midterm Exam")
        left_layout.addWidget(self.exam_input)
        
        left_layout.addWidget(QLabel(""))
        
        # Exam Date
        left_layout.addWidget(QLabel("Exam Date:"))
        date_layout = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))
        date_layout.addWidget(self.date_input)
        
        today_btn = QPushButton("Today")
        today_btn.clicked.connect(self.set_today)
        date_layout.addWidget(today_btn)
        left_layout.addLayout(date_layout)
        
        left_layout.addWidget(QLabel(""))
        
        # Number of Random Questions
        left_layout.addWidget(QLabel("Number of Questions:"))
        random_layout = QHBoxLayout()
        
        random_layout.addWidget(QLabel("Select"))
        self.random_count = QSpinBox()
        self.random_count.setMinimum(1)
        self.random_count.setMaximum(100)
        self.random_count.setValue(5)
        random_layout.addWidget(self.random_count)
        
        random_layout.addWidget(QLabel("random questions"))
        random_layout.addStretch()
        left_layout.addLayout(random_layout)
        
        left_layout.addWidget(QLabel(""))
        
        # Output Directory
        left_layout.addWidget(QLabel("Output Directory:"))
        output_layout = QHBoxLayout()
        self.output_input = QLineEdit()
        self.output_input.setText("output")
        output_layout.addWidget(self.output_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(browse_btn)
        left_layout.addLayout(output_layout)
        
        left_layout.addWidget(QLabel(""))
        
        # Action Buttons
        generate_btn = QPushButton("📄 Generate Papers (Random)")
        generate_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 12px; font-weight: bold; font-size: 12px;"
        )
        generate_btn.clicked.connect(self.generate_papers_random)
        left_layout.addWidget(generate_btn)
        
        generate_selected_btn = QPushButton("📄 Generate Papers (Selected)")
        generate_selected_btn.setStyleSheet(
            "background-color: #FF9800; color: white; padding: 12px; font-weight: bold; font-size: 12px;"
        )
        generate_selected_btn.clicked.connect(self.generate_papers_selected)
        left_layout.addWidget(generate_selected_btn)
        
        load_folder_btn = QPushButton("📂 Load Output Folder")
        load_folder_btn.clicked.connect(self.load_output_folder)
        left_layout.addWidget(load_folder_btn)
        
        left_layout.addWidget(QLabel(""))
        
        # Status
        left_layout.addWidget(QLabel("Status:"))
        self.status_label = QTextEdit()
        self.status_label.setReadOnly(True)
        self.status_label.setMaximumHeight(120)
        left_layout.addWidget(self.status_label)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        main_layout.addWidget(left_panel, 1)
        
        # ===== RIGHT PANEL - Questions =====
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("Questions from PDF:"))
        
        # Questions scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        questions_widget = QWidget()
        self.questions_layout = QVBoxLayout()
        
        self.question_checkboxes = {}
        self.update_questions_display()
        
        questions_widget.setLayout(self.questions_layout)
        scroll.setWidget(questions_widget)
        right_layout.addWidget(scroll)
        
        # Select/Deselect all buttons
        button_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("✓ Select All")
        select_all_btn.clicked.connect(self.select_all_questions)
        button_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("✗ Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all_questions)
        button_layout.addWidget(deselect_all_btn)
        
        randomize_btn = QPushButton("🎲 Randomize Selection")
        randomize_btn.clicked.connect(self.randomize_selection)
        button_layout.addWidget(randomize_btn)
        
        right_layout.addLayout(button_layout)
        
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(right_panel, 1)
        
        main_widget.setLayout(main_layout)
    
    def update_questions_display(self):
        """Update the questions checkbox display."""
        # Clear existing checkboxes
        while self.questions_layout.count():
            item = self.questions_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.question_checkboxes = {}
        
        if not self.loaded_questions:
            no_pdf = QLabel("⚠️ No PDF loaded. Click 'Load PDF' to get started.")
            no_pdf.setStyleSheet("color: gray; font-style: italic;")
            self.questions_layout.addWidget(no_pdf)
            return
        
        for qid in sorted(self.loaded_questions.keys()):
            question = self.loaded_questions[qid]
            q_text = question.get('question', 'Unknown')[:60]
            
            checkbox = QCheckBox(f"Q{qid}: {q_text}...")
            checkbox.setChecked(self.selected_questions.get(qid, False))
            checkbox.stateChanged.connect(lambda checked=None, q=qid: self.on_question_checked(q))
            
            self.question_checkboxes[qid] = checkbox
            self.questions_layout.addWidget(checkbox)
        
        self.questions_layout.addStretch()
    
    def on_question_checked(self, question_id):
        """Handle question checkbox state change."""
        checkbox = self.question_checkboxes.get(question_id)
        if checkbox:
            self.selected_questions[question_id] = checkbox.isChecked()
    
    def load_pdf(self):
        """Load PDF file and extract questions."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        self.pdf_path = file_path
        self.update_status(f"Loading: {Path(file_path).name}...")
        
        # Start loading thread
        self.loader_thread = PDFLoaderThread(file_path)
        self.loader_thread.progress.connect(self.update_status)
        self.loader_thread.finished.connect(self.pdf_loading_finished)
        self.loader_thread.start()
    
    def pdf_loading_finished(self, success, questions, message):
        """Handle PDF loading completion."""
        if success:
            self.loaded_questions = questions
            self.selected_questions = {}
            self.random_count.setMaximum(len(questions))
            self.random_count.setValue(min(5, len(questions)))
            
            self.pdf_label.setText(f"✓ {Path(self.pdf_path).name} ({len(questions)} questions)")
            self.pdf_label.setStyleSheet("color: green; font-weight: bold;")
            
            self.update_questions_display()
            self.update_status(f"✓ {message}")
            
            QMessageBox.information(
                self, "Success",
                f"Loaded {len(questions)} questions from PDF\n\nSelect questions and click 'Generate Papers'"
            )
        else:
            self.update_status(f"✗ Failed to load PDF: {message}")
            self.pdf_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Error", f"Failed to load PDF:\n{message}")
    
    def set_today(self):
        """Set date to today."""
        self.date_input.setText(datetime.now().strftime("%d-%m-%Y"))
    
    def browse_output_dir(self):
        """Browse for output directory."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.output_input.setText(folder)
    
    def select_all_questions(self):
        """Select all questions."""
        for qid, checkbox in self.question_checkboxes.items():
            checkbox.setChecked(True)
            self.selected_questions[qid] = True
    
    def deselect_all_questions(self):
        """Deselect all questions."""
        for qid, checkbox in self.question_checkboxes.items():
            checkbox.setChecked(False)
            self.selected_questions[qid] = False
    
    def randomize_selection(self):
        """Randomly select questions."""
        if not self.loaded_questions:
            QMessageBox.warning(self, "Error", "Please load a PDF first")
            return
        
        # Deselect all
        for checkbox in self.question_checkboxes.values():
            checkbox.setChecked(False)
        
        # Select random count
        count = self.random_count.value()
        available_ids = list(self.loaded_questions.keys())
        selected_ids = random.sample(available_ids, min(count, len(available_ids)))
        
        for qid in selected_ids:
            if qid in self.question_checkboxes:
                self.question_checkboxes[qid].setChecked(True)
                self.selected_questions[qid] = True
        
        self.update_status(f"✓ Randomly selected {len(selected_ids)} questions")
    
    def get_selected_questions(self):
        """Get IDs of selected questions."""
        selected = [qid for qid, is_selected in self.selected_questions.items() if is_selected]
        return selected
    
    def generate_papers_random(self):
        """Generate papers with random selection."""
        if not self.loaded_questions:
            QMessageBox.warning(self, "Error", "Please load a PDF first")
            return
        
        # Randomly select questions
        count = self.random_count.value()
        available_ids = list(self.loaded_questions.keys())
        
        if count > len(available_ids):
            QMessageBox.warning(
                self, "Error",
                f"Cannot select {count} questions. Only {len(available_ids)} available."
            )
            return
        
        selected_ids = random.sample(available_ids, count)
        questions = {qid: self.loaded_questions[qid] for qid in selected_ids}
        
        self._generate_documents(questions, f"Generated {count} random questions")
    
    def generate_papers_selected(self):
        """Generate papers with manually selected questions."""
        if not self.loaded_questions:
            QMessageBox.warning(self, "Error", "Please load a PDF first")
            return
        
        selected_ids = self.get_selected_questions()
        
        if not selected_ids:
            QMessageBox.warning(self, "Error", "Please select at least one question")
            return
        
        questions = {qid: self.loaded_questions[qid] for qid in selected_ids}
        self._generate_documents(questions, f"Generated {len(selected_ids)} selected questions")
    
    def _generate_documents(self, questions, message):
        """Generate documents with given questions."""
        # Validate inputs
        college_name = self.college_input.text().strip()
        exam_name = self.exam_input.text().strip()
        exam_date = self.date_input.text().strip()
        output_dir = self.output_input.text().strip()
        
        if not college_name:
            QMessageBox.warning(self, "Error", "Please enter College Name")
            return
        
        if not exam_name:
            QMessageBox.warning(self, "Error", "Please enter Exam Name")
            return
        
        self.update_status(message + "\n\nGenerating documents...\n")
        
        # Create and start thread
        self.generator_thread = DocumentGeneratorThread(
            college_name, exam_name, exam_date, questions, output_dir
        )
        self.generator_thread.progress.connect(self.update_status)
        self.generator_thread.finished.connect(self.generation_finished)
        self.generator_thread.start()
    
    def update_status(self, message):
        """Update status display."""
        current = self.status_label.toPlainText()
        self.status_label.setText(current + message + "\n")
        self.status_label.verticalScrollBar().setValue(
            self.status_label.verticalScrollBar().maximum()
        )
    
    def generation_finished(self, success, message):
        """Handle generation completion."""
        if success:
            self.update_status(f"\n✓ {message}")
            QMessageBox.information(self, "Success", message)
        else:
            self.update_status(f"\n✗ {message}")
            QMessageBox.critical(self, "Error", message)
    
    def load_output_folder(self):
        """Open output folder in file explorer."""
        output_dir = self.output_input.text().strip()
        if not Path(output_dir).exists():
            QMessageBox.warning(self, "Error", f"Directory not found: {output_dir}")
            return
        
        import platform
        import subprocess
        
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", output_dir])
        elif platform.system() == "Windows":
            os.startfile(output_dir)
        else:  # Linux
            subprocess.run(["xdg-open", output_dir])


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MCQPaperGeneratorGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
