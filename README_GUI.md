# MCQ Paper Generator - Desktop GUI Edition

## 📱 Overview

A professional desktop application for generating MCQ Question Papers and Answer Keys with built-in API key licensing system. Works on Windows, macOS, and Linux.

### ✨ Key Features

✅ **Beautiful Desktop GUI** - PyQt5 based interface  
✅ **API Key Licensing** - Secure distribution with license validation  
✅ **No Installation** - Portable executable, copy and run  
✅ **Text Input Fields** - College name, exam name, exam date  
✅ **Checkbox Questions** - Select which questions to include  
✅ **Batch Generation** - Generate both Question Paper and Answer Key at once  
✅ **Multi-Format Export** - Word (.docx) and PDF (.pdf)  
✅ **Question Management** - Add more questions easily  
✅ **Output Folder** - Direct access to generated documents  

---

## 🚀 Quick Start

### Option 1: Run from Source (Development)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (First time only) Generate a license
python license_generator.py

# 3. Run the application
python app.py
```

### Option 2: Use Standalone Executable (Distribution)

```bash
# Windows
MCQPaperGenerator.exe

# macOS/Linux
./MCQPaperGenerator
```

---

## 💻 GUI Features

### Input Fields
- **College Name** - Main heading of document
- **Exam Name** - Exam title
- **Exam Date** - Automatically set to today (editable)
- **Output Directory** - Where to save generated files

### Question Selection
- **Checkbox List** - All available questions with first 60 characters visible
- **Select All** - Quickly select all questions
- **Deselect All** - Clear all selections

### Action Buttons
- **Generate Papers** - Create Question Paper and Answer Key
- **Load Output Folder** - Open generated documents in file explorer

### Status Display
- Real-time progress messages
- Success/error notifications
- Link to output location

---

## 🔐 License System

### For Users

The application includes a license validation system:

1. **First Launch:** Application checks for `license.json`
2. **License Dialog:** Choose to load existing license or generate new one
3. **Validation:** Green message confirms valid license
4. **Access Granted:** Use application for full license period

### For Administrators

Generate and distribute licenses:

```bash
# Generate single license
python license_generator.py

# Generate multiple licenses at once
python license_generator.py batch licenses_batch.json

# List all licenses
python license_generator.py list
```

### License Details
- User name and email
- Expiry date (1 month to 1 year)
- API key for validation
- Active/inactive status

---

## 📦 Installation Methods

### Method 1: Direct Python Execution
```bash
git clone <repository>
cd "daddy project"
pip install -r requirements.txt
python app.py
```

### Method 2: Standalone Executable
1. Download `MCQPaperGenerator.zip`
2. Extract to any folder
3. Double-click executable or run from terminal
4. License validates automatically

### Method 3: Build Your Own
```bash
python build.py build
cd dist
./MCQPaperGenerator
```

---

## 🎨 GUI Layout

```
┌─────────────────────────────────────┬──────────────────────────────┐
│         INPUT PANEL                 │   QUESTIONS PANEL            │
│                                     │                              │
│ College Name:                       │ Select Questions:            │
│ [___________________________]        │ ☐ Q1: What is...             │
│                                     │ ☑ Q2: Which planet...        │
│ Exam Name:                          │ ☐ Q3: What is the...         │
│ [___________________________]        │ ☑ Q4: Who wrote...           │
│                                     │ ☐ Q5: What is the...         │
│ Exam Date:                          │ [Scroll Area]                │
│ [15-01-2026]  [Today]               │                              │
│                                     │ [Select All]  [Deselect All] │
│ Output Directory:                   │                              │
│ [output]  [Browse...]               │                              │
│                                     │                              │
│ [📄 Generate Papers]                │                              │
│ [📂 Load Output Folder]             │                              │
│                                     │                              │
│ Status:                             │                              │
│ ┌───────────────────────────┐       │                              │
│ │ Ready to generate...      │       │                              │
│ │ Generating documents...   │       │                              │
│ │ ✓ All files ready         │       │                              │
│ └───────────────────────────┘       │                              │
└─────────────────────────────────────┴──────────────────────────────┘
```

---

## 📝 Generated Documents

### Question Paper (DOCX/PDF)
- College name (main heading)
- Date and Exam Name (headers)
- Instructions section
- Numbered questions (Q1, Q2, etc.)
- Multiple choice options (A, B, C, D)
- Professional formatting

### Answer Key & Solutions (DOCX/PDF)
- Answer key table
- Detailed solutions
- Explanations for each answer
- Color-coded answers (green for correct)
- Professional formatting

### File Naming
```
Question_Paper_20260120_143022.docx
Question_Paper_20260120_143022.pdf
Answer_Key_Solutions_20260120_143022.docx
Answer_Key_Solutions_20260120_143022.pdf
```

---

## 🔧 Configuration

### Adding Custom Questions

Edit `database.py`:

```python
11: {
    "question": "Your question here?",
    "options": {
        "A": "Option 1",
        "B": "Option 2",
        "C": "Option 3",
        "D": "Option 4"
    },
    "correct_answer": "B",
    "explanation": "Why B is the correct answer..."
}
```

Reload application to see new questions.

### Customizing Document Style

Edit `document_generator.py`:
- Font sizes (lines 18, 22, etc.)
- Colors and styling
- Margins and spacing
- Header/footer content

---

## 🛠️ System Requirements

### Windows
- Windows 7 or later
- 512 MB RAM minimum
- 100 MB disk space
- Optional: Visual C++ Redistributable

### macOS
- macOS 10.12 (Sierra) or later
- 512 MB RAM minimum
- 100 MB disk space
- Terminal or double-click executable

### Linux
- Ubuntu 16.04 or later
- Python 3.7+ or use executable
- 512 MB RAM minimum
- 100 MB disk space

---

## 📚 User Guide

### Step-by-Step: Generate a Question Paper

1. **Launch Application**
   - Double-click MCQPaperGenerator
   - Wait for license validation

2. **Enter Details**
   - College Name: "XYZ University"
   - Exam Name: "Physics Midterm"
   - Exam Date: Auto-filled (edit if needed)

3. **Select Questions**
   - Check boxes for questions to include
   - Use "Select All" for all questions
   - Minimum 1 question required

4. **Generate**
   - Click "Generate Papers"
   - Wait for processing
   - See status: "✓ All documents generated"

5. **Access Files**
   - Click "Load Output Folder"
   - Files appear in Windows Explorer/Finder
   - Ready to share or print

---

## 🚨 Troubleshooting

### Issue: "No License Found"
**Solution:** 
- Ensure `license.json` in app folder
- Generate new license: `python license_generator.py`
- Copy license to app directory

### Issue: "License Expired"
**Solution:**
- Contact administrator for renewal
- New license can be generated

### Issue: PDF Not Generated
**Solution:**
- LibreOffice required for PDF conversion
- macOS: `brew install libreoffice`
- Windows: Install from libreoffice.org
- Linux: `sudo apt install libreoffice`

### Issue: Application Won't Start
**Solution (Windows):**
- Install Visual C++ Redistributable
- Run as Administrator
- Check Windows Defender settings

**Solution (Mac):**
- Allow in Security & Privacy settings
- Terminal: `xattr -d com.apple.quarantine MCQPaperGenerator`

**Solution (Linux):**
- Make executable: `chmod +x MCQPaperGenerator`
- Run: `./MCQPaperGenerator`

---

## 📊 Performance

- **Startup Time:** 2-3 seconds
- **Document Generation:** 1-2 seconds
- **PDF Conversion:** 3-5 seconds
- **Memory Usage:** ~100 MB

---

## 🔄 Updates

### Updating Questions
1. Edit `database.py`
2. Add new questions
3. Reload application

### Updating License
1. Generate new license file
2. Replace old `license.json`
3. Restart application

### New Version
1. Download new package
2. Replace executable
3. Keep license.json and license/ folder

---

## 📄 Files Reference

| File | Purpose |
|------|---------|
| `app.py` | Main launcher |
| `gui.py` | PyQt5 interface |
| `license_manager.py` | License handling |
| `database.py` | Questions database |
| `document_generator.py` | Word document creation |
| `pdf_converter.py` | PDF export |
| `license_generator.py` | License creation tool |

---

## 🎓 Education & Training

### For Teachers
- Quickly generate exam papers
- Different versions for different classes
- Professional formatting
- Easy to customize

### For Institutions
- Bulk distribute via license system
- No installation required
- Works offline
- Secure and portable

### For Students
- Generate practice papers
- Understand question patterns
- Self-study preparation
- Portable to any device

---

## 📞 Support

### Users
- Check QUICKSTART.md
- Review DISTRIBUTION_GUIDE.md
- Contact your administrator

### Administrators
- See license_manager.py documentation
- Use license_generator.py tool
- Refer to DISTRIBUTION_GUIDE.md

### Developers
- Build.py for creating executables
- gui.py for UI modifications
- See code comments for details

---

## 📄 License & Terms

This software is provided with license validation. Usage governed by the included license file.

---

## 🚀 Getting Help

1. **Check Documentation:**
   - README.md (full features)
   - QUICKSTART.md (fast start)
   - DISTRIBUTION_GUIDE.md (deployment)

2. **Common Issues:**
   - See Troubleshooting section above
   - Check license validity
   - Verify Python/dependencies installed

3. **Contact Support:**
   - Reach out to administrator
   - Provide license key ID
   - Include error messages

---

**Version:** 1.0.0 GUI Edition  
**Release Date:** January 20, 2026  
**Status:** ✅ Production Ready  
**Platform Support:** Windows, macOS, Linux
