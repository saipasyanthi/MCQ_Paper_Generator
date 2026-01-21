#!/usr/bin/env python3
"""
Main entry point for the MCQ Paper Generator GUI
Run this to launch the desktop application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == "__main__":
    main()
