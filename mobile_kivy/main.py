#!/usr/bin/env python3
"""
Kivy-based mobile app scaffold for MCQ Paper Generator.
Includes lightweight license check and local question storage.
This is a starting point for building an Android APK via Buildozer.
"""

import json
import csv
from datetime import datetime
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import mainthread
from kivy.core.window import Window


# ----------------------------
# License utilities
# ----------------------------
class LicenseError(Exception):
    pass


class LicenseManager:
    """Minimal license validator for mobile builds."""

    LICENSE_FILE = "license.json"

    @staticmethod
    def _load_license(path: Path):
        with path.open("r") as f:
            return json.load(f)

    @staticmethod
    def _find_license(user_dir: Path) -> Path | None:
        # 1) user data dir
        candidate = user_dir / LicenseManager.LICENSE_FILE
        if candidate.exists():
            return candidate
        # 2) app working dir
        candidate = Path.cwd() / LicenseManager.LICENSE_FILE
        if candidate.exists():
            return candidate
        # 3) packaged with app (same folder as this file)
        pkg_dir = Path(__file__).parent
        candidate = pkg_dir / LicenseManager.LICENSE_FILE
        if candidate.exists():
            return candidate
        candidate = pkg_dir / "default_license.json"
        if candidate.exists():
            return candidate
        return None

    @staticmethod
    def _ensure_copy_to_user_dir(src: Path, user_dir: Path) -> Path:
        """Copy license to user data dir so it persists."""
        user_dir.mkdir(parents=True, exist_ok=True)
        dest = user_dir / LicenseManager.LICENSE_FILE
        if not dest.exists():
            dest.write_bytes(src.read_bytes())
        return dest

    @staticmethod
    def validate(user_dir: Path):
        lic_path = LicenseManager._find_license(user_dir)
        if not lic_path:
            raise LicenseError("No license found. Please add license.json to the app folder.")

        # ensure we keep a local copy in user data dir for future runs
        if lic_path.parent != user_dir:
            lic_path = LicenseManager._ensure_copy_to_user_dir(lic_path, user_dir)

        try:
            data = LicenseManager._load_license(lic_path)
        except Exception as exc:  # noqa: BLE001
            raise LicenseError(f"Invalid license file. {exc}")

        # Check expiry
        expires_raw = data.get("expires")
        try:
            expires_dt = datetime.fromisoformat(expires_raw)
        except Exception:  # noqa: BLE001
            raise LicenseError("License expiry date is invalid.")

        if datetime.now() > expires_dt:
            days = (datetime.now() - expires_dt).days
            raise LicenseError(f"License expired {days} days ago.")

        if not data.get("is_active", False):
            raise LicenseError("License is inactive.")

        remaining = (expires_dt - datetime.now()).days
        return remaining, data


# ----------------------------
# Data store utilities
# ----------------------------
class QuestionStore:
    """Simple JSON-backed question store."""

    def __init__(self, user_dir: Path):
        self.user_dir = user_dir
        self.db_path = self.user_dir / "questions.json"
        self.questions: list[dict] = []
        self._load()

    def _load(self):
        if self.db_path.exists():
            try:
                with self.db_path.open("r") as f:
                    self.questions = json.load(f)
            except Exception:
                self.questions = []
        else:
            self.questions = []

    def _save(self):
        self.user_dir.mkdir(parents=True, exist_ok=True)
        with self.db_path.open("w") as f:
            json.dump(self.questions, f, indent=2)

    def add_question(self, question_text: str, options: list[str], correct_idx: int, subject: str, chapter: str, difficulty: str):
        q = {
            "id": len(self.questions) + 1,
            "question": question_text,
            "options": options,
            "correct_answer": correct_idx,
            "subject": subject,
            "chapter": chapter,
            "difficulty": difficulty,
        }
        self.questions.append(q)
        self._save()
        return q

    def all_questions(self) -> list[dict]:
        return list(self.questions)

    def export_json(self, path: Path | None = None) -> Path:
        target = path or (self.user_dir / "questions_export.json")
        target.write_text(json.dumps(self.questions, indent=2))
        return target

    def export_csv(self, path: Path | None = None) -> Path:
        target = path or (self.user_dir / "questions_export.csv")
        with target.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "question", "option_a", "option_b", "option_c", "option_d", "correct_idx", "subject", "chapter", "difficulty"])
            for q in self.questions:
                opts = q.get("options", ["", "", "", ""])
                writer.writerow([
                    q.get("id", ""),
                    q.get("question", ""),
                    opts[0] if len(opts) > 0 else "",
                    opts[1] if len(opts) > 1 else "",
                    opts[2] if len(opts) > 2 else "",
                    opts[3] if len(opts) > 3 else "",
                    q.get("correct_answer", ""),
                    q.get("subject", ""),
                    q.get("chapter", ""),
                    q.get("difficulty", ""),
                ])
        return target

    def export_txt(self, path: Path | None = None) -> Path:
        target = path or (self.user_dir / "questions_export.txt")
        lines = []
        for q in self.questions:
            lines.append(f"Q{q.get('id','')}: {q.get('question','')}")
            opts = q.get("options", [])
            for idx, opt in enumerate(opts):
                mark = "*" if idx == q.get("correct_answer", -1) else " "
                lines.append(f"  {mark} {chr(65+idx)}. {opt}")
            lines.append(f"  Subject: {q.get('subject','')} | Chapter: {q.get('chapter','')} | Difficulty: {q.get('difficulty','')}")
            lines.append("")
        target.write_text("\n".join(lines))
        return target


# ----------------------------
# Screens
# ----------------------------
class HomeScreen(Screen):
    license_message = StringProperty("")


class AddQuestionScreen(Screen):
    subject_input = ObjectProperty(None)
    chapter_input = ObjectProperty(None)
    difficulty_input = ObjectProperty(None)
    question_input = ObjectProperty(None)
    option_a = ObjectProperty(None)
    option_b = ObjectProperty(None)
    option_c = ObjectProperty(None)
    option_d = ObjectProperty(None)
    correct_spinner = ObjectProperty(None)


class BankScreen(Screen):
    questions = ListProperty([])

    def on_questions(self, *args):
        self.update_bank()

    def update_bank(self):
        grid = self.ids.get("bank_grid")
        if not grid:
            return
        grid.clear_widgets()
        if not self.questions:
            grid.add_widget(Label(text="No questions yet."))
            return
        for q in self.questions:
            grid.add_widget(Label(text=f"Q{q['id']}: {q['question']}", bold=True, text_size=(grid.width, None), halign="left"))
            for idx, opt in enumerate(q["options"]):
                prefix = "✔ " if idx == q.get("correct_answer") else "  "
                grid.add_widget(Label(text=f"{prefix}{chr(65+idx)}. {opt}", text_size=(grid.width, None), halign="left"))
            grid.add_widget(Label(text=f"Subject: {q['subject']} | Chapter: {q['chapter']} | Difficulty: {q['difficulty']}", font_size="12sp", text_size=(grid.width, None), halign="left"))
            grid.add_widget(Label(text="---", color=(0.6, 0.6, 0.6, 1)))


class GenerateScreen(Screen):
    # Placeholder for future export/generation workflow
    pass


class PDFQuestionScreen(Screen):
    questions = ListProperty([])
    checked_indices = ListProperty([])

    def on_questions(self, *_):
        self.checked_indices = []
        self.update_view()

    def update_view(self):
        grid = self.ids.get("pdf_grid")
        if not grid:
            return
        grid.clear_widgets()
        if not self.questions:
            grid.add_widget(Label(
                text="No PDF attached yet.\n\nClick 'Add PDF' to load questions.",
                size_hint_y=None,
                height=dp(80),
                halign="center"
            ))
            return
        
        for idx, text in enumerate(self.questions):
            # Create a container for each question
            container = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(80),  # Increased height for better readability
                spacing=dp(10),
                padding=(dp(8), dp(4))
            )
            
            # Checkbox on left
            checkbox = CheckBox(
                size_hint=(None, None),
                width=dp(40),
                height=dp(40),
                active=(idx in self.checked_indices)
            )
            checkbox.bind(active=lambda cb, val, i=idx: self._toggle_check(i, val))
            container.add_widget(checkbox)
            
            # Question text on right with wrapping
            # Truncate very long questions for mobile
            display_text = text[:200] + "..." if len(text) > 200 else text
            
            label = Label(
                text=f"[b]Q{idx+1}:[/b] {display_text}",
                markup=True,
                size_hint_x=1,
                size_hint_y=None,
                height=dp(70),
                text_size=(None, None),  # Let it calculate size
                halign="left",
                valign="top",
                font_size="13sp"
            )
            # Bind to calculate proper text_size after width is known
            label.bind(width=lambda lbl, w: setattr(lbl, 'text_size', (w, None)))
            container.add_widget(label)
            
            grid.add_widget(container)

    def _toggle_check(self, idx: int, active: bool):
        if active and idx not in self.checked_indices:
            self.checked_indices.append(idx)
        elif not active and idx in self.checked_indices:
            self.checked_indices.remove(idx)


class RootManager(ScreenManager):
    pass


# ----------------------------
# Main App
# ----------------------------
class MCQMobileApp(App):
    title = "MCQ Paper Generator"
    attached_pdf = StringProperty("")
    pdf_questions = ListProperty([])
    
    # Form fields for paper generation
    college_name = StringProperty("")
    exam_name = StringProperty("")
    exam_date = StringProperty(datetime.now().strftime("%d-%m-%Y"))
    num_questions = 5
    output_dir = StringProperty("")

    def build(self):
        # Set background to white for the whole app
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("app.kv")
        self.user_dir = Path(self.user_data_dir)
        self.output_dir = str(self.user_dir / "output")
        self.store = QuestionStore(self.user_dir)
        manager = RootManager()
        self._validate_license(manager)
        existing_pdf = self.user_dir / "questions_import.pdf"
        if existing_pdf.exists():
            self.attach_pdf(existing_pdf, show_popup=False)
        return manager

    @mainthread
    def _popup(self, title: str, message: str):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def _validate_license(self, root_manager: RootManager):
        try:
            remaining, data = LicenseManager.validate(self.user_dir)
            msg = f"License valid for {remaining} days (User: {data.get('user_name','N/A')})"
            home = root_manager.get_screen("home")
            home.license_message = msg
        except LicenseError as exc:
            self._popup("License Required", str(exc))
            raise SystemExit(1)

    def on_start(self):
        # populate PDF list if available
        self.refresh_pdf_screen()

    def attach_pdf(self, pdf_path: Path, show_popup: bool = True):
        if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
            self._popup("Invalid file", "Please select a PDF file.")
            return
        self.user_dir.mkdir(parents=True, exist_ok=True)
        dest = self.user_dir / "questions_import.pdf"
        dest.write_bytes(pdf_path.read_bytes())
        self.attached_pdf = str(dest)
        self.load_pdf_questions(dest)
        if show_popup:
            self._popup("PDF added", f"Stored a copy at:\n{dest}\nParsed {len(self.pdf_questions)} lines")

    def open_pdf_picker(self):
        chooser = FileChooserListView(filters=["*.pdf"], path=str(Path.home()))
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)

        popup = Popup(title="Select PDF", content=layout, size_hint=(0.9, 0.9))

        def do_attach(*_):
            if chooser.selection:
                self.attach_pdf(Path(chooser.selection[0]))
            popup.dismiss()

        btn_attach = Button(text="Attach")
        btn_attach.bind(on_release=do_attach)
        btn_cancel = Button(text="Cancel")
        btn_cancel.bind(on_release=lambda *_: popup.dismiss())

        buttons.add_widget(btn_attach)
        buttons.add_widget(btn_cancel)
        layout.add_widget(chooser)
        layout.add_widget(buttons)
        popup.open()

    def open_output_dir_picker(self):
        """Let the user choose where generated files are saved."""
        start_path = Path(self.output_dir) if self.output_dir else Path.home()
        chooser = FileChooserListView(path=str(start_path), dirselect=True)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)

        popup = Popup(title="Select Output Folder", content=layout, size_hint=(0.9, 0.9))

        def do_set(*_):
            if chooser.selection:
                chosen = Path(chooser.selection[0])
                # If user picked a file, use its parent; if folder, use it directly
                selected_dir = chosen if chosen.is_dir() else chosen.parent
                selected_dir.mkdir(parents=True, exist_ok=True)
                self.output_dir = str(selected_dir)
                self._popup("Output Folder Set", f"Files will save to:\n{selected_dir}")
            popup.dismiss()

        btn_set = Button(text="Set Folder")
        btn_set.bind(on_release=do_set)
        btn_cancel = Button(text="Cancel")
        btn_cancel.bind(on_release=lambda *_: popup.dismiss())

        buttons.add_widget(btn_set)
        buttons.add_widget(btn_cancel)
        layout.add_widget(chooser)
        layout.add_widget(buttons)
        popup.open()

    def load_pdf_questions(self, pdf_path: Path):
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except Exception:
            self._popup("Missing dependency", "PyPDF2 not installed. Add PyPDF2 to requirements for PDF parsing.")
            return

        try:
            reader = PdfReader(str(pdf_path))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
            full_text = "\n".join(text_parts)
            
            # Parse questions intelligently
            questions = self._parse_questions_from_text(full_text)
            
            if not questions:
                self._popup("No questions found", "Could not find any questions in the PDF. Questions should be numbered (e.g., '1.', 'Q1:', '1)', etc.)")
                return
                
            self.pdf_questions = questions
            self.refresh_pdf_screen()
            self._popup("PDF loaded", f"Found {len(questions)} questions")
        except Exception as exc:  # noqa: BLE001
            self._popup("PDF error", f"Could not read PDF. {exc}")

    def _parse_questions_from_text(self, text: str) -> list:
        """Extract questions from PDF text with their options."""
        import re
        
        lines = text.split('\n')
        questions = []
        current_block = []
        
        # Pattern to identify question starts
        question_start = r'^\s*(\d+)\s*[\.\)]\s+'
        
        # Patterns to skip (headers only)
        skip_patterns = [
            r'college|university|exam.*:|date.*:|time|marks|instructions',
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip header lines
            should_skip = False
            for pattern in skip_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    should_skip = True
                    break
            if should_skip:
                continue
            
            # Check if new question starts
            if re.match(question_start, line):
                # Save previous question block
                if current_block:
                    questions.append('\n'.join(current_block))
                    current_block = []
                # Start new question
                current_block.append(line)
            elif current_block:
                # Add line to current question (could be continuation or option)
                current_block.append(line)
        
        # Add last question
        if current_block:
            questions.append('\n'.join(current_block))
        
        return questions

    def refresh_pdf_screen(self):
        if not self.root:
            return
        screen: PDFQuestionScreen = self.root.get_screen("pdf")
        screen.questions = list(self.pdf_questions)

    def select_all_pdf_questions(self):
        """Select all PDF questions."""
        if not self.root:
            return
        screen: PDFQuestionScreen = self.root.get_screen("pdf")
        screen.checked_indices = list(range(len(self.pdf_questions)))
        screen.update_view()

    def clear_all_pdf_questions(self):
        """Clear all PDF question selections."""
        if not self.root:
            return
        screen: PDFQuestionScreen = self.root.get_screen("pdf")
        screen.checked_indices = []
        screen.update_view()

    def generate_random_paper(self):
        """Generate paper with randomly selected questions."""
        if not self.pdf_questions:
            self._popup("No PDF", "Please load a PDF first.")
            return
        if not self.college_name or not self.exam_name:
            self._popup("Missing info", "Please fill in college name and exam name.")
            return
        
        import random
        count = min(self.num_questions, len(self.pdf_questions))
        selected = random.sample(range(len(self.pdf_questions)), count)
        selected_qs = [self.pdf_questions[i] for i in selected]
        
        self._save_generated_paper(selected_qs, "random")

    def generate_selected_paper(self):
        """Generate paper with checked questions."""
        if not self.pdf_questions:
            self._popup("No PDF", "Please load a PDF first.")
            return
        if not self.college_name or not self.exam_name:
            self._popup("Missing info", "Please fill in college name and exam name.")
            return
        
        screen: PDFQuestionScreen = self.root.get_screen("pdf")
        if not screen.checked_indices:
            self._popup("No selection", "Please check at least one question.")
            return
        
        selected_qs = [self.pdf_questions[i] for i in sorted(screen.checked_indices)]
        self._save_generated_paper(selected_qs, "selected")

    def _save_generated_paper(self, questions: list, mode: str):
        """Save generated paper and answer key as PDF files."""
        from datetime import datetime as dt
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        except ImportError:
            # Fallback to text if reportlab not available
            self._save_as_text(questions, mode)
            return
        
        # Create output directory (user-selected)
        output_dir = Path(self.output_dir) if self.output_dir else Path.cwd() / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
        question_file = output_dir / f"Question_Paper_{timestamp}.pdf"
        answer_file = output_dir / f"Answer_Key_Solutions_{timestamp}.pdf"
        
        styles = getSampleStyleSheet()
        
        # Create Question Paper
        doc = SimpleDocTemplate(str(question_file), pagesize=letter)
        story = []
        
        # Header
        story.append(Paragraph(f"<b>{self.college_name}</b>", styles['Title']))
        story.append(Paragraph(f"<b>Exam: {self.exam_name}</b>", styles['Heading2']))
        story.append(Paragraph(f"Date: {self.exam_date}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Questions
        for q in questions:
            story.append(Paragraph(q.replace('\n', '<br/>'), styles['Normal']))
            story.append(Spacer(1, 15))
        
        doc.build(story)
        
        # Create Answer Key
        doc_ans = SimpleDocTemplate(str(answer_file), pagesize=letter)
        story_ans = []
        
        story_ans.append(Paragraph(f"<b>Answer Key - {self.exam_name}</b>", styles['Title']))
        story_ans.append(Spacer(1, 20))
        
        # Extract answers (look for correct answer pattern)
        import re
        for idx, q in enumerate(questions, 1):
            # Try to find the answer in common formats
            answer = "Not specified"
            lines = q.split('\n')
            for line in lines:
                # Look for patterns like "Answer: A" or "Correct: B"
                match = re.search(r'(answer|correct)[:\s]+([A-D])', line, re.IGNORECASE)
                if match:
                    answer = match.group(2).upper()
                    break
            story_ans.append(Paragraph(f"Question {idx}: <b>{answer}</b>", styles['Normal']))
            story_ans.append(Spacer(1, 10))
        
        doc_ans.build(story_ans)

        # Also create text versions (questions + answer key)
        self._save_text_outputs(output_dir, questions, timestamp)
        
        self._popup("Papers Generated", f"Created:\n• {question_file.name}\n• {answer_file.name}")
    
    def _save_as_text(self, questions: list, mode: str):
        """Fallback: Save as text file."""
        from datetime import datetime as dt
        
        # Create output directory (user-selected)
        output_dir = Path(self.output_dir) if self.output_dir else Path.cwd() / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
        self._save_text_outputs(output_dir, questions, timestamp, show_popup=True)

    def _save_text_outputs(self, output_dir: Path, questions: list, timestamp: str, show_popup: bool = False):
        """Save question paper and answer key as text files."""
        q_filename = output_dir / f"Question_Paper_{timestamp}.txt"
        a_filename = output_dir / f"Answer_Key_Solutions_{timestamp}.txt"

        # Question paper text
        q_lines = [
            f"College: {self.college_name}",
            f"Exam: {self.exam_name}",
            f"Date: {self.exam_date}",
            "",
            "Questions:",
            "=" * 60,
            "",
        ]
        for idx, q in enumerate(questions, 1):
            q_lines.append(f"Q{idx}.")
            q_lines.append(q)
            q_lines.append("")
        q_filename.write_text("\n".join(q_lines))

        # Answer key text
        a_lines = [
            f"Exam: {self.exam_name}",
            f"Date: {self.exam_date}",
            "",
            "Answer Key:",
            "=" * 40,
            "",
        ]
        for idx, q in enumerate(questions, 1):
            ans = self._extract_answer_from_question(q)
            a_lines.append(f"Q{idx}: {ans}")
        a_filename.write_text("\n".join(a_lines))

        if show_popup:
            self._popup("Text Files Generated", f"Saved to:\n• {q_filename.name}\n• {a_filename.name}\n\nInstall 'reportlab' for PDF output.")

    @staticmethod
    def _extract_answer_from_question(question_text: str) -> str:
        """Best-effort answer extraction from question block."""
        import re
        # Look for explicit answer markers
        match = re.search(r'(answer|correct)[:\s]+([A-D])', question_text, re.IGNORECASE)
        if match:
            return match.group(2).upper()
        # If no marker, leave as TBD
        return "Not specified"


if __name__ == "__main__":
    MCQMobileApp().run()
