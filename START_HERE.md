# 🚀 START HERE - MCQ PAPER GENERATOR

## Choose Your Role

### 👤 I'm an END USER (I have the app already)
→ Go to: **QUICK START FOR USERS** (below)

### 🏢 I'm an ADMINISTRATOR (Need to deploy)
→ Go to: **INSTALLATION_GUIDE.md**

### 👨‍💻 I'm a DEVELOPER (Want to customize)
→ Go to: **README_GUI.md** then **README.md**

---

## QUICK START FOR USERS

### If You Have `MCQPaperGenerator.exe` or `MCQPaperGenerator`

#### Step 1️⃣ Prepare Files
```
Create a folder:
📁 My Applications
  ├── MCQPaperGenerator.exe    (or MCQPaperGenerator on Mac/Linux)
  ├── license.json             (should be included)
  └── output/                  (will be created automatically)
```

#### Step 2️⃣ Run Application

**Windows:**
- Double-click `MCQPaperGenerator.exe`

**macOS:**
- Double-click `MCQPaperGenerator`
- Or: Right-click → Open (if security warning)

**Linux:**
- Terminal: `./MCQPaperGenerator`

#### Step 3️⃣ Use the Application

The window shows:

```
LEFT PANEL (Input)           RIGHT PANEL (Questions)
─────────────────            ──────────────────────
College Name: [____]         ☐ Q1: Capital of France
Exam Name:    [____]         ☑ Q2: Red Planet
Exam Date:    [____]         ☐ Q3: Chemical symbol
Output:       [folder]       ☐ Q4: Shakespeare
                             ☑ Q5: Largest ocean
[Generate]                   
[Open Folder]                [Select All] [Deselect]

Status:
Generating...
✓ Complete!
```

#### Step 4️⃣ Generate Your Paper

1. **Enter College Name**
   - Example: "XYZ University"

2. **Enter Exam Name**
   - Example: "Physics - Midterm"

3. **Date** (auto-filled, can change)
   - Format: DD-MM-YYYY

4. **Select Questions**
   - Check boxes for questions you want
   - Minimum 1 required

5. **Click "Generate Papers"**
   - Wait for ✓ message

6. **Click "Load Output Folder"**
   - Your documents appear
   - Files ready to print/share

#### ✅ You're Done!

Generated files:
- `Question_Paper_XXXXXX.docx` - For students
- `Question_Paper_XXXXXX.pdf` - For printing
- `Answer_Key_Solutions_XXXXXX.docx` - For teachers
- `Answer_Key_Solutions_XXXXXX.pdf` - For printing

---

## COMMON QUESTIONS

### Q: Why do I need a license file?
**A:** It protects the software and ensures it's used by authorized users only.

### Q: Can I use it without internet?
**A:** Yes! Everything is offline. Just need license.json.

### Q: Can I add my own questions?
**A:** Contact your administrator. They can customize and rebuild.

### Q: How long does it take to generate papers?
**A:** 2-5 seconds for typical papers.

### Q: What if the app won't start?
**A:** Check:
1. license.json is in same folder
2. You have permission to run it
3. See Troubleshooting section below

### Q: Can I use on Mac and Windows?
**A:** You need the right version for your OS. Ask administrator.

---

## TROUBLESHOOTING

### Problem: "License not found"
```
✗ No license found. Please add license.json file.
```
**Solution:**
- Ensure license.json in app directory
- Contact administrator if missing

### Problem: "License expired"
```
✗ License expired 30 days ago.
```
**Solution:**
- Ask administrator for new license
- Replace old license.json

### Problem: App won't start (Windows)
```
Error: Visual C++ Runtime
```
**Solution:**
- Download: Visual C++ Redistributable (microsoft.com)
- Install and retry

### Problem: "Permission denied" (Mac/Linux)
```
zsh: permission denied: ./MCQPaperGenerator
```
**Solution:**
- Terminal: `chmod +x MCQPaperGenerator`
- Then: `./MCQPaperGenerator`

### Problem: PDF not generated
```
⚠ Documents generated (PDF conversion skipped)
```
**Solution:**
- LibreOffice required for PDF
- Or use DOCX file in Word

---

## FILE FORMATS

### DOCX (Word Format)
- ✅ Edit in Microsoft Word
- ✅ Edit in Google Docs
- ✅ Edit in LibreOffice

### PDF (Portable Format)
- ✅ Print directly
- ✅ Email easily
- ✅ View on any device
- ❌ Cannot edit easily

---

## SAMPLE QUESTIONS IN DATABASE

The application includes 10 sample questions:

1. What is the capital of France?
2. Which planet is known as the Red Planet?
3. What is the chemical symbol for Gold?
4. Who wrote 'Romeo and Juliet'?
5. What is the largest ocean on Earth?
6. Which element has atomic number 6?
7. In which year did the Titanic sink?
8. What is the smallest prime number?
9. Which country is home to the Great Wall?
10. What is the powerhouse of the cell?

---

## TIPS & TRICKS

### Tip 1: Pre-fill College Name
Ask administrator to customize default in code

### Tip 2: Save Favorite Configurations
Write down your usual settings

### Tip 3: Batch Generate
Generate multiple papers with different questions

### Tip 4: Organization
Create separate output folders per exam:
```
📁 2026_Exams
  ├── Physics_Midterm/
  ├── Chemistry_Final/
  └── Biology_Quiz/
```

### Tip 5: Backup Important Papers
Keep copies of generated papers

---

## WHAT TO DO IF STUCK

**Option 1: Check Documentation**
- README_GUI.md (Features)
- QUICKSTART.md (Quick ref)

**Option 2: Verify Installation**
- Confirm license.json present
- Check file permissions
- Restart application

**Option 3: Contact Administrator**
- Share error message
- Include your license key ID
- Describe what you were doing

---

## SUPPORT LEVEL MATRIX

| Issue | Solution |
|-------|----------|
| How to use? | This guide |
| License error? | Contact administrator |
| Want more questions? | Contact administrator |
| Found a bug? | Contact administrator |
| Need Python? | Administrator should provide exe |

---

## NEXT STEPS

### Right Now
1. ✅ Extract application
2. ✅ Verify license.json present
3. ✅ Run application
4. ✅ Test with one question

### Then
1. 📋 Generate your first real paper
2. 📁 Save to organized folder
3. 🖨️ Print or share as needed
4. ✍️ Get feedback from users

---

## KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| Ctrl+A / Cmd+A | Select All Questions |
| Ctrl+D / Cmd+D | (Deselect all not available) |
| Enter | Generate Papers (after selecting questions) |
| Ctrl+O / Cmd+O | Open Output Folder |

---

## FREQUENTLY CALLED COMMANDS

```bash
# Shouldn't need these, but in case:

# On Mac/Linux, if app won't start:
chmod +x MCQPaperGenerator
./MCQPaperGenerator

# On Windows, run as administrator:
Right-click MCQPaperGenerator.exe
Select "Run as administrator"
```

---

## GETTING HELP

### Online Resources Included
- README_GUI.md - Full feature list
- INSTALLATION_GUIDE.md - Installation help
- PROJECT_SUMMARY.md - What's included

### Offline Help
- Check status bar in app
- Read error messages carefully
- Try the FAQ above

### Contact Your Administrator
- Explain the problem
- Share error message
- Include license key ID

---

## CONFIRMATION

You're ready if:

✅ You have MCQPaperGenerator executable  
✅ You have license.json file  
✅ You can run the application  
✅ You understand how to select questions  
✅ You know where output files go  

---

## 5-MINUTE TUTORIAL

**Minute 1:** Extract files, verify license.json  
**Minute 2:** Run application  
**Minute 3:** Enter college and exam details  
**Minute 4:** Select 3-4 questions with checkboxes  
**Minute 5:** Click "Generate" and view results  

**Result:** Professional question paper ready!

---

## QUICK REFERENCE CARD

```
╔════════════════════════════════════════╗
║   MCQ PAPER GENERATOR                  ║
║   Quick Reference                     ║
╠════════════════════════════════════════╣
║ STEP 1: Extract + Run app            ║
║ STEP 2: Enter college and exam names ║
║ STEP 3: Select questions (checkbox)  ║
║ STEP 4: Click Generate               ║
║ STEP 5: View in output folder        ║
║                                      ║
║ OUTPUT: .docx + .pdf files           ║
║ READY: Print or share!               ║
╚════════════════════════════════════════╝
```

---

## 🎯 YOU'RE ALL SET!

Enjoy generating professional question papers! 🎓

---

**Version:** 1.0.0  
**Last Updated:** January 20, 2026  
**Status:** Production Ready ✅

*For detailed info, see README_GUI.md*
