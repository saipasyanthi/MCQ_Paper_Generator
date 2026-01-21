# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd "daddy project"
pip install -r requirements.txt
```

### Step 2: (Optional) Install LibreOffice for PDF Support
```bash
# macOS
brew install libreoffice

# Ubuntu/Debian
sudo apt-get install libreoffice
```

### Step 3: Run the Application
```bash
python main.py
```

### Step 4: Follow the Interactive Menu
```
1. Select "Generate Question Paper and Answer Key"
2. Enter: College Name → Exam Name → Date → Question Numbers
3. Select comma-separated question numbers (e.g., 1,3,5,7)
4. Documents are saved to the "output/" folder
```

---

## 📋 Sample Workflow

### Example Input
```
College Name: ABC University
Exam Name: Physics - Midterm Exam
Date: 20-01-2026
Questions: 1,3,5,7
```

### Output Files
- ✅ Question_Paper_20260120_143022.docx
- ✅ Question_Paper_20260120_143022.pdf
- ✅ Answer_Key_Solutions_20260120_143022.docx
- ✅ Answer_Key_Solutions_20260120_143022.pdf

---

## 🔧 Programmatic Usage

Use `example_usage.py` to generate papers without the interactive menu:

```bash
python example_usage.py
```

Or import in your own script:

```python
from database import get_questions
from document_generator import QuestionPaperGenerator, AnswerKeyGenerator

questions = get_questions([1, 2, 3, 4, 5])

qp = QuestionPaperGenerator("My College", "Exam 1", "20-01-2026", questions)
qp.generate("output/question_paper.docx")

ak = AnswerKeyGenerator("My College", "Exam 1", "20-01-2026", questions)
ak.generate("output/answer_key.docx")
```

---

## 📚 View Available Questions

Select Option 2 from the main menu to see all 10 sample questions in the database:

1. Geography - Capital of France
2. Astronomy - Red Planet
3. Chemistry - Element Symbol
4. Literature - Shakespeare
5. Geography - Largest Ocean
6. Chemistry - Atomic Number
7. History - Titanic Sinking
8. Mathematics - Prime Number
9. Geography - Great Wall
10. Biology - Cell Powerhouse

---

## 🎨 Document Features

### Question Paper Includes:
- College name (18pt, bold, centered)
- Date and Exam Name (side by side)
- Instructions section
- All questions with options A-D
- Professional formatting

### Answer Key Includes:
- Answer key table (compact format)
- Detailed solutions with explanations
- Correct answers highlighted in green
- Professional formatting

---

## ⚙️ Customization

### Add More Questions
Edit `database.py` and add to `QUESTIONS_DATABASE`:

```python
11: {
    "question": "Your question here?",
    "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
    "correct_answer": "B",
    "explanation": "Why this answer is correct."
}
```

### Modify Document Settings
Edit `config.py` to customize fonts, colors, and margins.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| PDF conversion fails | Install LibreOffice: `brew install libreoffice` |
| Invalid question IDs | Check Option 2 to see available questions |
| Permission denied | Run `chmod +x main.py` on macOS/Linux |

---

## 📖 Full Documentation

See `README.md` for comprehensive documentation including:
- Detailed feature list
- API reference
- Project structure
- Future enhancements

---

**Version:** 1.0.0  
**Python:** 3.7+  
**Last Updated:** January 20, 2026
