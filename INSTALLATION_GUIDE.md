# INSTALLATION & DEPLOYMENT GUIDE

## 📋 Table of Contents
1. [For Users (Pre-Built App)](#for-users-pre-built-app)
2. [For Administrators (Build & Deploy)](#for-administrators-build--deploy)
3. [For Developers (From Source)](#for-developers-from-source)
4. [Troubleshooting](#troubleshooting)

---

## For Users (Pre-Built App)

If you received a `MCQPaperGenerator` executable file, follow this:

### Installation (All Platforms)

1. **Extract Package**
   ```
   MCQPaperGenerator.zip
   ├── MCQPaperGenerator.exe  (Windows)
   ├── MCQPaperGenerator      (Mac/Linux)
   └── license.json           (License file)
   ```

2. **Place Files Together**
   - Extract to any folder
   - Keep `MCQPaperGenerator` and `license.json` in same directory
   - Create `output` folder if needed

3. **Run Application**

   **Windows:**
   - Double-click `MCQPaperGenerator.exe`
   - Or: `MCQPaperGenerator.exe`

   **macOS:**
   - Double-click `MCQPaperGenerator`
   - Or in Terminal: `./MCQPaperGenerator`
   - If security warning: Right-click → Open

   **Linux:**
   - Terminal: `./MCQPaperGenerator`
   - If permission error: `chmod +x MCQPaperGenerator`

4. **License Validation**
   - First run: license.json auto-loaded
   - Green status = valid license
   - If error: Ensure license.json in same folder

5. **Start Using**
   - Enter college name and exam details
   - Select questions via checkboxes
   - Click "Generate Papers"
   - View in output folder

### Troubleshooting (Users)

**"Cannot find license.json"**
- Ensure license.json in app folder
- Contact administrator for license

**"License expired"**
- Contact administrator for renewal

**"Application won't start"**
- Windows: Install Visual C++ Redistributable
- Mac: Allow in Security settings
- Linux: Check permissions with `chmod +x`

---

## For Administrators (Build & Deploy)

### Prerequisites
```bash
# Install Python 3.7+
# Install pip
# Install Git (optional)
```

### Step 1: Get Source Code

```bash
# Option A: Clone repository
git clone <repository-url>
cd "daddy project"

# Option B: Download ZIP and extract
unzip mcq-generator-main.zip
cd "daddy project"
```

### Step 2: Setup Development Environment

**macOS/Linux:**
```bash
chmod +x setup.sh
bash setup.sh
```

**Windows:**
```bash
setup.bat
```

### Step 3: Generate License

```bash
python license_generator.py
```

Follow the prompts:
- Enter user name
- Enter email
- Select validity (1 month to 1 year)
- License saved to `licenses/` folder

### Step 4: Build Executable

```bash
pip install pyinstaller

# Build for current platform
python build.py build
```

Creates: `dist/MCQPaperGenerator`

### Step 5: Package for Distribution

**macOS/Linux:**
```bash
# Copy license
cp licenses/license_*.json dist/license.json

# Create archive
cd dist
tar -czf MCQPaperGenerator.tar.gz MCQPaperGenerator license.json
```

**Windows:**
```batch
REM Copy license
copy licenses\license_*.json dist\license.json

REM Create ZIP using:
REM - Windows Explorer: Right-click → Send to → Compressed folder
REM - Or use 7-Zip/WinRAR
```

### Step 6: Distribute

Share the package:
- Email the archive
- File hosting service
- Internal repository
- USB drive

---

## For Developers (From Source)

### Clone Repository

```bash
git clone <repository-url>
cd "daddy project"
```

### Setup Environment

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Application

```bash
# Generate license (first time)
python license_generator.py

# Run GUI application
python app.py
```

### Development Tasks

**Add New Questions:**
```python
# Edit database.py
11: {
    "question": "Your question?",
    "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
    "correct_answer": "B",
    "explanation": "..."
}
```

**Modify GUI:**
- Edit `gui.py`
- PyQt5 documentation: https://doc.qt.io/qtforpython

**Customize Documents:**
- Edit `document_generator.py`
- python-docx docs: https://python-docx.readthedocs.io

**Build Executable:**
```bash
python build.py build      # Build
python build.py clean      # Clean
```

---

## Architecture Overview

```
MCQ Generator System
│
├── User Layer (GUI)
│   └── gui.py (PyQt5 Interface)
│
├── License Layer
│   ├── license_manager.py (License validation)
│   └── license_generator.py (License creation)
│
├── Business Logic
│   ├── database.py (Questions)
│   ├── document_generator.py (DOCX creation)
│   └── pdf_converter.py (PDF export)
│
└── Distribution
    ├── app.py (Entry point)
    ├── build.py (PyInstaller script)
    └── setup.sh/setup.bat (Installation)
```

---

## File Structure

```
MCQPaperGenerator/
│
├── Core Files
│   ├── app.py                     # Main entry point
│   ├── gui.py                     # PyQt5 GUI
│   ├── database.py                # Questions (10 samples)
│   ├── document_generator.py      # Word generation
│   └── pdf_converter.py           # PDF export
│
├── License System
│   ├── license_manager.py         # License handling
│   └── license_generator.py       # License creation tool
│
├── Build & Setup
│   ├── build.py                   # Build script
│   ├── setup.sh                   # Mac/Linux setup
│   ├── setup.bat                  # Windows setup
│   └── requirements.txt           # Python dependencies
│
├── Documentation
│   ├── README.md                  # Original CLI docs
│   ├── README_GUI.md              # GUI application docs
│   ├── QUICKSTART.md              # Quick start guide
│   ├── DISTRIBUTION_GUIDE.md      # Distribution info
│   └── INSTALLATION_GUIDE.md      # This file
│
├── Runtime
│   ├── licenses/                  # Generated license files
│   ├── output/                    # Generated documents
│   └── license.json               # Active license
│
└── Executables (after build)
    └── dist/
        └── MCQPaperGenerator      # Standalone executable
```

---

## Configuration

### Application Settings

Edit `config.py`:
```python
DEFAULT_COLLEGE_NAME = "Your Institution"
OUTPUT_DIRECTORY = "output"
DOCUMENT_SETTINGS = {
    "question_font_size": 11,
    "option_font_size": 10,
    # ... more settings
}
```

### Database Settings

Edit `database.py`:
- Add/modify questions
- Change question format
- Add new question types

### License Settings

Edit `license_manager.py`:
- License validity periods
- Validation rules
- License format

---

## Security Considerations

### License Protection
- Licenses are JSON files (not encrypted by default)
- For higher security: Implement encryption in `license_manager.py`
- API keys are not stored in executables

### Distribution Security
- Use HTTPS for downloads
- Verify file integrity with checksums
- Keep source code in private repository

### User Privacy
- License contains: Name, Email, Expiry Date
- No tracking or analytics
- Offline operation

---

## Performance Notes

### Startup
- First launch: 2-3 seconds (license validation)
- Subsequent: 1-2 seconds

### Document Generation
- 5 questions: 1-2 seconds
- 10 questions: 2-3 seconds
- PDF conversion: Add 3-5 seconds

### Memory
- Application: ~100 MB RAM
- Per document: ~10 MB
- Total: ~150-200 MB for typical use

---

## System Requirements

### Minimum
- **OS:** Windows 7, macOS 10.12, Ubuntu 16.04+
- **RAM:** 512 MB
- **Disk:** 100 MB
- **CPU:** 1 GHz dual-core

### Recommended
- **OS:** Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **RAM:** 2-4 GB
- **Disk:** 200 MB
- **CPU:** 2+ GHz multi-core

### Optional
- **LibreOffice:** For PDF conversion
- **Microsoft Word/Adobe:** For document editing

---

## Batch Operations

### Generate Multiple Licenses

Create `batch_licenses.json`:
```json
{
    "licenses": [
        {
            "user_name": "User 1",
            "user_email": "user1@example.com",
            "expiry_days": 365
        },
        {
            "user_name": "User 2",
            "user_email": "user2@example.com",
            "expiry_days": 180
        }
    ]
}
```

Run:
```bash
python license_generator.py batch batch_licenses.json
```

---

## Updates & Maintenance

### Update Application
1. Download new version
2. Replace executable
3. Keep existing licenses (backward compatible)

### Update Questions
1. Edit `database.py`
2. Add new questions
3. Restart application

### Renew Licenses
1. Generate new license
2. Distribute to users
3. Replace old `license.json`

---

## Support & Troubleshooting

See complete troubleshooting in README_GUI.md

### Common Issues

| Issue | Solution |
|-------|----------|
| License error | Regenerate and redistribute |
| PDF not working | Install LibreOffice |
| GUI slow | Check RAM, close other apps |
| Questions not showing | Restart app after adding |

---

## Quick Reference

### Command Cheat Sheet

```bash
# Development
python app.py                       # Run GUI
python license_generator.py         # Create license
python license_generator.py list    # List licenses

# Build & Deploy
python build.py build              # Create executable
python build.py clean              # Remove build files

# Setup
bash setup.sh                       # Mac/Linux setup
setup.bat                          # Windows setup
```

---

## Version History

**v1.0.0** (January 20, 2026)
- Initial desktop GUI release
- License system implemented
- Multi-platform support
- 10 sample questions included

---

**Last Updated:** January 20, 2026  
**Status:** Production Ready  
**Platforms:** Windows, macOS, Linux
