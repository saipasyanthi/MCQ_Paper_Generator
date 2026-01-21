# Sample Configuration File
# You can customize these defaults before running the application

# Default College Name
DEFAULT_COLLEGE_NAME = "ABC University"

# Default Exam Names (add more as needed)
EXAM_NAMES = [
    "Midterm Exam",
    "Final Exam",
    "Quiz",
    "Assignment",
    "Semester Exam"
]

# Output Directory
OUTPUT_DIRECTORY = "output"

# Document Settings
DOCUMENT_SETTINGS = {
    "question_font_size": 11,      # Font size for questions
    "option_font_size": 10,        # Font size for options
    "heading_font_size": 18,       # Font size for main heading
    "subheading_font_size": 12,    # Font size for subheadings
    "page_margins": 1,             # Page margins in inches
}

# PDF Conversion Settings
PDF_CONVERSION = {
    "enabled": True,               # Enable PDF conversion
    "timeout": 30,                 # Timeout in seconds
    "quality": "high"              # Conversion quality
}
