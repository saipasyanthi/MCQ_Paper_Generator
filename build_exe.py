#!/usr/bin/env python3
"""
Build script to create executable for MCQ Paper Generator
Supports Windows (.exe), macOS (.app), and Linux (binary)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """Clean previous build files."""
    print("Cleaning previous builds...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  Removed {d}/")
    
    # Remove spec files
    for spec in Path('.').glob('*.spec'):
        spec.unlink()
        print(f"  Removed {spec}")

def create_executable():
    """Create executable using PyInstaller."""
    print("\n" + "="*60)
    print("Building MCQ Paper Generator Executable")
    print("="*60 + "\n")
    
    # PyInstaller command
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--name=MCQ_Paper_Generator',
        '--onefile',
        '--noconsole',
        '--add-data=license.json:.',
        '--hidden-import=PyQt5',
        '--hidden-import=reportlab',
        '--hidden-import=docx',
        '--hidden-import=pymupdf',
        '--hidden-import=pdfplumber',
        '--hidden-import=PIL',
        'app.py'
    ]
    
    print("Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        
        # Find the executable
        dist_dir = Path('dist')
        if dist_dir.exists():
            exe_files = list(dist_dir.glob('MCQ_Paper_Generator*'))
            if exe_files:
                exe_path = exe_files[0]
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                
                print(f"\nExecutable created: {exe_path}")
                print(f"File size: {size_mb:.1f} MB")
                print(f"\nLocation: {exe_path.absolute()}")
                print("\nYou can now distribute this file!")
                print("Users just need to:")
                print("  1. Copy the executable to their computer")
                print("  2. Double-click to run")
                print("  3. No Python installation required!")
                
                return True
    else:
        print("\n" + "="*60)
        print("BUILD FAILED!")
        print("="*60)
        return False

def main():
    """Main build process."""
    print("MCQ Paper Generator - Executable Builder\n")
    
    # Check if license exists
    if not os.path.exists('license.json'):
        print("WARNING: license.json not found!")
        print("The executable will require users to provide their own license.json file.\n")
    
    # Clean previous builds
    clean_build()
    
    # Create executable
    success = create_executable()
    
    if success:
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("\n1. Test the executable:")
        print("   - Navigate to the 'dist' folder")
        print("   - Run the MCQ_Paper_Generator executable")
        print("\n2. Distribution:")
        print("   - Share the file from the 'dist' folder")
        print("   - Include license.json if needed")
        print("   - No other files required!")
        print("\n" + "="*60)
    else:
        print("\nBuild failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
