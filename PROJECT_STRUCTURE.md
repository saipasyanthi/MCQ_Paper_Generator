# Project File Structure & Description

## 📁 Project Directory: `/Users/pasi/daddy project`

```
daddy project/
├── main.py                      ⭐ Main application (Run this!)
├── database.py                  📊 10 sample MCQ questions
├── document_generator.py        📄 Word document generation
├── pdf_converter.py             🔄 DOCX to PDF converter
├── example_usage.py             💡 Programmatic usage example
├── config.py                    ⚙️  Configuration settings
├── requirements.txt             📦 Python dependencies
├── README.md                    📖 Full documentation
├── QUICKSTART.md               🚀 Quick start guide (read first!)
└── output/                      📁 Generated documents (auto-created)
```

---

## 📄 File Details

### **main.py** - Main Application
- **Purpose:** Interactive CLI application
- **How to run:** `python main.py`
- **Features:**
  - Main menu with 3 options
  - Collect user input (college, exam, date, questions)
  - Generate both DOCX and PDF documents
  - Display output paths

### **database.py** - Question Database
- **Contains:** 10 sample MCQ questions
- **Functions:**
  - `get_question(id)` - Get single question
  - `get_questions(ids)` - Get multiple questions
  - `validate_question_ids(ids)` - Validate IDs
  - `get_all_questions()` - Get all questions
  - `get_available_question_ids()` - List available IDs

### **document_generator.py** - Document Generation
- **Classes:**
  - `QuestionPaperGenerator` - Creates question paper DOCX
  - `AnswerKeyGenerator` - Creates answer key DOCX
- **Features:**
  - Professional formatting
  - Header with college name and exam details
  - Properly styled questions and options
  - Answer key table and detailed solutions

### **pdf_converter.py** - PDF Conversion
- **Class:** `PDFConverter`
- **Methods:**
  - `docx_to_pdf()` - Convert single DOCX to PDF
  - `convert_documents()` - Convert both papers to PDF
- **Requires:** LibreOffice installed

### **example_usage.py** - Usage Example
- **Purpose:** Shows how to use the generator without CLI
- **How to run:** `python example_usage.py`
- **Shows:** Programmatic generation of sample papers

### **config.py** - Configuration
- **Contains:** Customizable settings
- **Options:**
  - Default college name
  - Document formatting (fonts, sizes)
  - PDF conversion settings
  - Exam names list

### **requirements.txt** - Dependencies
```
python-docx==0.8.11
reportlab==4.0.7
pypdf==3.17.1
Pillow==10.0.1
```

### **README.md** - Full Documentation
- Complete feature list
- Installation instructions
- Usage guide
- Database management
- API reference
- Troubleshooting
- Future enhancements

### **QUICKSTART.md** - Quick Reference
- 5-minute setup
- Sample workflow
- Customization tips
- Troubleshooting table

---

## 🎯 Features Overview

| Feature | File | Status |
|---------|------|--------|
| Interactive CLI | main.py | ✅ Complete |
| Database with 10 questions | database.py | ✅ Complete |
| Question Paper generation | document_generator.py | ✅ Complete |
| Answer Key generation | document_generator.py | ✅ Complete |
| Word (.docx) export | document_generator.py | ✅ Complete |
| PDF export | pdf_converter.py | ✅ Complete |
| Comma-separated input | main.py | ✅ Complete |
| College name heading | document_generator.py | ✅ Complete |
| Date & Exam name headers | document_generator.py | ✅ Complete |
| Professional formatting | document_generator.py | ✅ Complete |

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python main.py

# 3. Follow prompts
# Enter: College Name → Exam → Date → Questions
# Specify questions: 1,3,5,7

# 4. Find output files
# Files are in: output/ directory
```

---

## 💻 System Requirements

- **Python:** 3.7 or higher
- **OS:** macOS, Linux, or Windows
- **Memory:** 200MB free
- **LibreOffice:** (Optional) For PDF conversion

---

## 📋 Data Flow

```
User Input
    ↓
main.py (Collect data)
    ↓
database.py (Fetch questions)
    ↓
document_generator.py
    ├→ QuestionPaperGenerator → Question_Paper.docx
    └→ AnswerKeyGenerator → Answer_Key.docx
    ↓
pdf_converter.py (Optional)
    ├→ Question_Paper.pdf
    └→ Answer_Key.pdf
    ↓
output/ (Save files)
```

---

## 🔧 Extending the Project

### Add More Questions
Edit `database.py` - Add entries to `QUESTIONS_DATABASE` dict

### Modify Document Format
Edit `document_generator.py` - Customize fonts, colors, spacing

### Change Output Directory
Edit `main.py` or `config.py` - Modify `OUTPUT_DIRECTORY`

### Add Database Backend
Create `database_backend.py` - Connect to SQLite/MySQL

---

## 📞 Support

1. Check **QUICKSTART.md** for common issues
2. Review **README.md** for detailed docs
3. Check code comments for implementation details
4. Run `python example_usage.py` for example workflow

---

**Project Created:** January 2026  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
