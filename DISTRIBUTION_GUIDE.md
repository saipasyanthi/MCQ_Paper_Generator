# DISTRIBUTION GUIDE

## 📦 Package Contents

```
MCQPaperGenerator/
├── app.exe / app (Windows/Mac/Linux executable)
├── license.json              (License file - provided by administrator)
├── README.md                 (Full documentation)
├── QUICKSTART.md             (Quick start guide)
└── output/                   (Auto-created for generated documents)
```

---

## 🚀 Installation & Setup

### For Users (License Holders)

#### **Step 1: Download the Package**
- Receive the MCQPaperGenerator package from the administrator
- Includes the application and license file

#### **Step 2: Extract Files**
```bash
# Windows/Mac/Linux
unzip MCQPaperGenerator.zip
cd MCQPaperGenerator
```

#### **Step 3: Run Application**

**Windows:**
- Double-click `MCQPaperGenerator.exe`

**macOS:**
- Double-click `MCQPaperGenerator` or run in terminal:
```bash
./MCQPaperGenerator
```

**Linux:**
```bash
./MCQPaperGenerator
```

#### **Step 4: License Validation**
- On first run, application auto-validates `license.json`
- Green status message means you're licensed
- If license expires, administrator must provide renewal

---

## 🔐 License Management (Administrator)

### Generate New License

```bash
# Interactive mode
python license_generator.py

# Follow prompts:
# - Enter user name
# - Enter user email
# - Select license validity (1 month to 1 year)
```

### Batch Generate Licenses

Create `licenses_batch.json`:
```json
{
    "licenses": [
        {
            "user_name": "John Doe",
            "user_email": "john@example.com",
            "expiry_days": 365
        },
        {
            "user_name": "Jane Smith",
            "user_email": "jane@example.com",
            "expiry_days": 180
        }
    ]
}
```

Then run:
```bash
python license_generator.py batch licenses_batch.json
```

### List All Licenses
```bash
python license_generator.py list
```

---

## 📋 Building from Source (Developers)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Build Executable
```bash
python build.py build
```

This creates:
- `dist/MCQPaperGenerator` (standalone executable)

### Step 3: Create Package
```bash
# Copy license file to dist/
cp license.json dist/

# Zip the folder
zip -r MCQPaperGenerator.zip dist/
```

---

## 🔄 Distribution Workflow

### For Administrators

```
1. Generate License
   └─ python license_generator.py
   └─ Creates: licenses/license_XXXXX.json

2. Build Application
   └─ python build.py build
   └─ Creates: dist/MCQPaperGenerator

3. Prepare Package
   └─ Copy license.json to dist/
   └─ Create dist/README.md
   └─ Zip dist/ folder

4. Distribute
   └─ Share MCQPaperGenerator.zip with users
   └─ Users extract and run
```

### For Users

```
1. Extract Package
   └─ unzip MCQPaperGenerator.zip
   └─ cd MCQPaperGenerator

2. Run Application
   └─ ./MCQPaperGenerator (Mac/Linux)
   └─ MCQPaperGenerator.exe (Windows)

3. License Validated Automatically
   └─ Ready to use!
```

---

## 🎯 Usage Scenario

### Example: University Distribution

**Administrator Does:**
1. Generate license for each department
2. Build GUI application
3. Package with license files
4. Distribute to faculty/students

**Users Do:**
1. Install package (simple folder copy)
2. Run application (double-click or terminal)
3. Generate question papers
4. Export to Word and PDF

**Result:**
- No installation hassles
- Works on any machine with license
- Portable and self-contained
- No internet required

---

## 🛠️ System Requirements

### Minimum Requirements
- **RAM:** 512 MB
- **Disk:** 100 MB
- **OS:** Windows 7+, macOS 10.12+, Ubuntu 16.04+

### Recommended
- **RAM:** 2 GB
- **Disk:** 200 MB
- **OS:** Windows 10+, macOS 10.15+, Ubuntu 20.04+

### Optional
- **LibreOffice:** For PDF conversion (auto-install recommended)

---

## 📝 License File Format

```json
{
    "key_id": "A1B2C3D4",
    "api_key": "your_long_api_key_here",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "created": "2026-01-20T10:30:00",
    "expires": "2027-01-20T10:30:00",
    "is_active": true,
    "machine_id": null
}
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "License not found" | Ensure license.json is in app directory |
| "License expired" | Contact administrator for renewal |
| "App won't start" | Download .NET Runtime (Windows) or check permissions |
| "PDF not generated" | Install LibreOffice or use DOCX format |

---

## 📞 Support

- **Users:** Contact your administrator
- **Administrators:** Review README.md and license_manager.py
- **Developers:** Check gui.py and build.py

---

## 📋 Files & Their Purpose

| File | Purpose |
|------|---------|
| `app.py` | Main entry point |
| `gui.py` | PyQt5 GUI code |
| `license_manager.py` | License system |
| `license_generator.py` | License creation tool |
| `database.py` | Question database |
| `document_generator.py` | Document creation |
| `pdf_converter.py` | PDF export |
| `build.py` | Build executable |

---

**Version:** 1.0.0 GUI Edition  
**Last Updated:** January 20, 2026  
**Status:** Production Ready
