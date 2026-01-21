# MCQ Paper Generator (Android - Kivy)

This is a Kivy-based mobile scaffold to build an Android APK.

## Status
- Basic screens: Home, Add Question, Question Bank, Export (JSON/CSV)
- Local JSON question storage in app data directory
- License check: reads `license.json` from user data, working dir, or bundled copy (auto-copies into user data on first run)
- Export: JSON, CSV, and TXT (saved in app storage)

## Run on desktop (for testing)
```bash
pip install -r requirements.txt
python main.py
```

## Build APK with Buildozer (Linux recommended)
1) Install system deps (example for Ubuntu):
```bash
sudo apt update
sudo apt install -y python3-venv build-essential git zip unzip openjdk-17-jdk
pip install --user buildozer cython
```
2) From `mobile_kivy/` run:
```bash
buildozer init   # already provided, but safe to rerun
buildozer -v android debug
```
3) The APK will be in `bin/` (e.g., `bin/MCQPaper-0.1-debug.apk`).

## License placement
The app bundles a `license.json`. On first run it copies it into user data. You can replace it by placing your own `license.json` either in the working directory or user data before first launch.

## Next steps to make it feature-complete
- Implement export to DOCX/PDF on Android (ensure libs are pure-Python; heavy libs may be difficult to package).
- Add PDF question extraction (pymupdf/pdfplumber may not be mobile-friendly; consider server-side extraction or simpler parsing).
- Improve UI/UX and add offline caching/backup.
- Add sync/backup endpoint if needed.

## Notes
- Buildozer works best on Linux. For macOS/Windows, use WSL2 or a Linux VM.
- Keep dependencies minimal for Android compatibility.
