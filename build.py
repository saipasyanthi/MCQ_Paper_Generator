#!/usr/bin/env python3
"""
Build script to create standalone executables
Requires PyInstaller to be installed
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def build_executable(platform_name=None):
    """Build standalone executable."""
    
    if platform_name is None:
        import platform
        platform_name = platform.system()
    
    print("\n" + "="*60)
    print(f"Building MCQ Generator for {platform_name}")
    print("="*60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller not found")
        print("Install it with: pip install pyinstaller")
        return False
    
    # Clean previous builds
    if Path("build").exists():
        print("Cleaning previous build...")
        shutil.rmtree("build")
    
    if Path("dist").exists():
        shutil.rmtree("dist")
    
    # Build command
    build_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=MCQPaperGenerator",
        "--icon=icon.ico" if Path("icon.ico").exists() else "",
        "--add-data=database.py:.",
        "--add-data=document_generator.py:.",
        "--add-data=pdf_converter.py:.",
        "--add-data=license_manager.py:.",
        "--hidden-import=PyQt5",
        "app.py"
    ]
    
    # Remove empty strings
    build_cmd = [x for x in build_cmd if x]
    
    print(f"\nRunning: {' '.join(build_cmd)}\n")
    
    try:
        result = subprocess.run(build_cmd, capture_output=False)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✓ BUILD SUCCESSFUL!")
            print("="*60)
            print("\nExecutable location:")
            print(f"  {os.path.abspath('dist/MCQPaperGenerator')}")
            print("\nTo distribute:")
            print("  1. Include license.json in the same directory")
            print("  2. Zip/package the folder")
            print("  3. Share with users")
            
            return True
        else:
            print("Build failed!")
            return False
    
    except Exception as e:
        print(f"Error during build: {str(e)}")
        return False


def create_installer():
    """Create installer using the built executable."""
    print("\nCreating installer...")
    
    if not Path("dist/MCQPaperGenerator").exists():
        print("Error: Executable not found. Build first!")
        return False
    
    # Copy additional files
    print("Copying additional files...")
    
    for file in ["README.md", "QUICKSTART.md", "LICENSE"]:
        if Path(file).exists():
            shutil.copy(file, "dist/")
    
    print("✓ Installer prepared in 'dist/' directory")
    return True


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            success = build_executable()
            if success and len(sys.argv) > 2 and sys.argv[2] == "package":
                create_installer()
        elif sys.argv[1] == "clean":
            print("Cleaning build artifacts...")
            for folder in ["build", "dist", "__pycache__"]:
                if Path(folder).exists():
                    shutil.rmtree(folder)
            print("✓ Cleaned")
        else:
            print("Usage: python build.py [build|clean]")
    else:
        build_executable()


if __name__ == "__main__":
    main()
