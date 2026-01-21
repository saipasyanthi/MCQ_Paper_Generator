# MCQ Paper Generator - PDF Edition 2.0

## 🎯 NEW FEATURES - PDF Question Loading

### What's New

This is a completely updated version that reads questions directly from your PDF file!

#### Key Features

✅ **Load PDF Button** - Click to upload your PDF containing questions  
✅ **Auto-Extract Questions** - Automatically reads and parses all questions from PDF  
✅ **Display Questions** - Shows all extracted questions in checkboxes  
✅ **Manual Selection** - Choose specific questions with checkboxes  
✅ **Random Generation** - Generate papers with random question selection  
✅ **Answer Key Creation** - Auto-generates answer keys and solutions  
✅ **Multi-Format Export** - Creates Word (.docx) and PDF (.pdf) files  

---

## 🚀 How to Use (Simple Steps)

### Step 1: Load Your PDF
1. Click **"Load PDF"** button (blue button on the left)
2. Select your PDF file containing MCQ questions
3. Application reads the PDF and extracts all questions

### Step 2: View Questions
- Right panel shows all extracted questions
- Each question displayed as a checkbox
- Shows first 60 characters of each question

### Step 3: Select Questions (Choose One)

**Option A: Generate Random Papers**
- Set number in "Select X random questions" spinner
- Click **"Generate Papers (Random)"** button
- App randomly selects specified number of questions

**Option B: Select Manually**
- Check boxes next to questions you want
- Use "Select All" or "Deselect All" buttons
- Use "Randomize Selection" to pick random ones
- Click **"Generate Papers (Selected)"** button

### Step 4: Fill in Exam Details
- **College Name**: Your institution name (becomes main heading)
- **Exam Name**: Exam title
- **Exam Date**: Auto-filled, can edit
- **Output Directory**: Where to save files

### Step 5: Generate Documents
- Click one of the Generate buttons
- Watch status messages
- System creates Question Paper + Answer Key
- Exports to DOCX and PDF formats

### Step 6: Access Generated Files
- Click **"Load Output Folder"** button
- Your files open in File Explorer/Finder
- Ready to print or share

---

## 📄 PDF Format Requirements

### Your PDF should contain questions like:

```
Q1. What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid
Answer: B
Explanation: Paris is the capital...

Q2. Which planet is known as the Red Planet?
A) Venus
B) Jupiter
C) Mars
D) Saturn
Answer: C
```

### Supported Formats

The system recognizes:
- **Question markers**: Q1, 1., Question:, etc.
- **Option markers**: A), B), C), D) or A. B. C. D.
- **Answer indicators**: Answer:, Correct:, Solution:
- **Explanations**: Optional but supported

---

## 🎨 GUI Layout

```
┌─────────────────────────────────────┬──────────────────────────┐
│     LEFT PANEL (Input & Controls)   │  RIGHT PANEL (Questions) │
│                                     │                          │
│ Question Paper Generator            │ Questions from PDF:      │
│                                     │                          │
│ 📄 Load PDF:                        │ ☐ Q1: What is...         │
│ [No PDF loaded] [Load PDF]          │ ☑ Q2: Which planet...    │
│                                     │ ☐ Q3: What is the...     │
│ College Name:                       │ ☑ Q4: Who wrote...       │
│ [__________________]                │ ☐ Q5: What is the...     │
│                                     │ [Scroll Area]            │
│ Exam Name:                          │                          │
│ [__________________]                │ [✓ Select All]           │
│                                     │ [✗ Deselect All]         │
│ Exam Date:                          │ [🎲 Randomize Selection] │
│ [20-01-2026] [Today]                │                          │
│                                     │                          │
│ Number of Questions:                │                          │
│ Select [5] random questions         │                          │
│                                     │                          │
│ Output Directory:                   │                          │
│ [output] [Browse...]                │                          │
│                                     │                          │
│ [📄 Generate Papers (Random)]       │                          │
│ [📄 Generate Papers (Selected)]     │                          │
│ [📂 Load Output Folder]             │                          │
│                                     │                          │
│ Status:                             │                          │
│ ┌──────────────────────────┐        │                          │
│ │ Loading: questions.pdf   │        │                          │
│ │ ✓ Loaded 50 questions    │        │                          │
│ │ Generating documents...  │        │                          │
│ │ ✓ All files ready        │        │                          │
│ └──────────────────────────┘        │                          │
└─────────────────────────────────────┴──────────────────────────┘
```

---

## 🔄 Generation Modes

### Mode 1: Random Generation
```
1. Load PDF with N questions
2. Set "Select X random questions" (e.g., 5)
3. Click "Generate Papers (Random)"
4. System randomly picks 5 questions
5. Creates Question Paper + Answer Key
```

### Mode 2: Manual Selection
```
1. Load PDF
2. Check specific question boxes
3. Click "Generate Papers (Selected)"
4. System uses only selected questions
5. Creates Question Paper + Answer Key
```

### Mode 3: Smart Randomization
```
1. Load PDF
2. Click "Randomize Selection"
3. Auto-selects random questions (count in spinner)
4. Click "Generate Papers (Selected)"
5. Creates papers with pre-randomized set
```

---

## 📊 Generated Files

### Question Paper
```
XYZ UNIVERSITY
Date: 20-01-2026       Exam: Physics - Midterm

INSTRUCTIONS:
- Answer all questions
- Each carries 1 mark
- Choose one best answer

Q1. What is the capital of France?
A) London  B) Paris  C) Berlin  D) Madrid

Q2. Which planet is known as the Red Planet?
A) Venus  B) Jupiter  C) Mars  D) Saturn

(... more questions ...)

Total Questions: 5
```

### Answer Key & Solutions
```
XYZ UNIVERSITY - Answer Key & Solutions
Date: 20-01-2026       Exam: Physics - Midterm

ANSWER KEY:
Q1: B    Q2: C    Q3: A    Q4: B    Q5: D

DETAILED SOLUTIONS:

Q1. What is the capital of France?
Answer: B
Explanation: Paris is the capital and most populous city of France...

Q2. Which planet is known as the Red Planet?
Answer: C
Explanation: Mars is often called the Red Planet...

(... more explanations ...)
```

---

## 🎲 Random Selection Examples

### Example 1: 10 Questions, Generate 5 Random
```
Original PDF: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10

First Generation: Q3, Q7, Q1, Q9, Q5 (random)
↓ Creates Question Paper 1 with these 5

Second Generation: Q2, Q8, Q4, Q10, Q6 (different random)
↓ Creates Question Paper 2 with these 5

Result: Two different papers from same PDF!
```

### Example 2: Manual + Random Combination
```
PDF: 20 questions available

Manually select: Q1, Q3, Q5, Q7, Q9, Q11, Q13, Q15, Q17, Q19 (10 selected)

Click "Randomize Selection" with count=5:
↓ Randomly picks 5 from your 10 selected

Results: Q3, Q9, Q15, Q1, Q13 (random from your selection)
```

---

## ✨ Smart Features

### Auto-Detection
- Recognizes question patterns automatically
- Works with various PDF formats
- Extracts options A, B, C, D
- Detects answer indicators

### Validation
- Checks question format
- Validates 4 options present
- Ensures correct answer marked
- Reports any malformed questions

### Threading
- Non-blocking PDF loading
- Doesn't freeze GUI
- Progress status updates
- Smooth experience

---

## ⚠️ PDF Quality Tips

### For Best Results:
✅ **Clear formatting** - Questions clearly separated  
✅ **Standard options** - A), B), C), D) format  
✅ **Marked answers** - Include "Answer: B" line  
✅ **Good text** - OCR-quality PDFs recommended  
✅ **Organization** - One question per section  

### Problems to Avoid:
❌ **Scanned images** - Cannot extract text from image PDFs  
❌ **Poor formatting** - Options mixed with text  
❌ **Multiple columns** - May extract in wrong order  
❌ **Missing answers** - Set defaults if needed  

---

## 🔧 How PDF Extraction Works

### Step 1: Extract Text
```
PDF File → pdfplumber → All text extracted → Page by page
```

### Step 2: Parse Questions
```
Text → Regex patterns → Find question markers
                     → Find options A-D
                     → Find answers
                     → Find explanations
```

### Step 3: Validate
```
Parsed data → Check format → Valid questions dict
                          → Ready for generation
```

### Step 4: Generate
```
Questions → Document Generator → Word document (.docx)
                              → PDF conversion → PDF file
```

---

## 📋 Typical Workflow

```
1. Prepare PDF with questions
   ↓
2. Launch application
3. Enter license validation
   ↓
4. Click "Load PDF"
5. Select your PDF file
   ↓
6. Application reads PDF
7. Shows extracted questions
   ↓
8. Enter exam details
   - College name
   - Exam name
   - Date
   ↓
9. Choose generation mode
   - Random: Spinner count + Generate Random
   - Manual: Check boxes + Generate Selected
   ↓
10. Click Generate button
11. Wait for completion
    ↓
12. View generated files
    Question Paper.docx
    Question Paper.pdf
    Answer Key.docx
    Answer Key.pdf
    ↓
13. Print or share files
```

---

## 🎯 Use Cases

### Case 1: Teacher Creating Quiz
```
1. Prepare PDF with 50 questions
2. Load PDF in application
3. Generate 10 random questions
4. Print for quiz
5. Generate answer key
6. Done in 2 minutes!
```

### Case 2: Multiple Test Versions
```
1. Load same PDF three times
2. Generate 20 random questions each
3. Create three different papers
4. All from same question bank
5. Prevents cheating!
```

### Case 3: Topic-Based Selection
```
1. Load PDF with mixed questions
2. Manually select only Physics questions
3. Generate paper with selected
4. Create focused exam
```

---

## 🆘 Troubleshooting

### "PDF won't load"
**Solution**: Ensure it's an actual PDF (not image-based), has extractable text

### "No questions found"
**Solution**: Check PDF format, ensure clear Q/A structure, verify text is readable

### "Options not recognized"
**Solution**: Ensure options are marked A), B), C), D) or similar format

### "Answers missing"
**Solution**: Add "Answer: B" lines to PDF, or use manual entry

### "Generation failed"
**Solution**: Verify college name entered, check output folder permissions

---

## 📞 Support

### Quick Help
1. Check this file - PDF Edition guide
2. See README_GUI.md - General features
3. Review START_HERE.md - Quick start

### Common Issues
- See Troubleshooting section above
- Check PDF format requirements
- Verify license.json present

---

## 🎉 Summary

The PDF Edition 2.0 includes:

✅ **Load PDF** - Click button to upload  
✅ **Auto-Extract** - Gets questions automatically  
✅ **Display** - Shows in checkboxes  
✅ **Select** - Manual or random  
✅ **Generate** - Creates papers + answer keys  
✅ **Export** - Word + PDF formats  

**All in a beautiful, user-friendly GUI!**

---

**Version:** 2.0 PDF Edition  
**Release Date:** January 20, 2026  
**Status:** ✅ Production Ready

*Now with direct PDF loading and intelligent question extraction!*
