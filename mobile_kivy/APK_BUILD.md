# MCQ Paper Generator - Android APK Build Guide

## Feature Parity with Desktop App

The Kivy mobile app now mirrors all core features of the desktop executable:

### Desktop Features → Mobile Implementation

| Feature | Desktop (PyQt5) | Mobile (Kivy) |
|---------|-----------------|---------------|
| **PDF Loading** | File dialog → extract questions | File picker → PyPDF2 text extraction |
| **Question List** | Scrollable list with checkboxes | Scrollable grid with checkboxes |
| **College/Exam/Date** | Text input fields | TextInput widgets |
| **Random Selection** | Spinbox (1-100) questions | Spinner (1-20) questions |
| **Generate Papers** | Random & Selected modes | Random & Selected modes |
| **Output Format** | DOCX → PDF | Plain text (.txt) |
| **License Check** | On startup | On app start |
| **Question Bank** | Manage locally | Manage locally |

## Building APK on macOS

### Prerequisites

1. **Android SDK** and **NDK** (via Android Studio or standalone)
2. **Java Development Kit (JDK)** 11 or 17
3. **Buildozer** for automated builds

```bash
pip install buildozer cython
```

### Build Steps

#### 1. Prepare on Linux/WSL (macOS cannot directly build APK)

If on macOS, use **WSL2** or a Linux VM:

```bash
# On Linux/WSL
cd /Users/pasi/MCQ_Paper_Generator/mobile_kivy

# Install build dependencies
sudo apt-get update
sudo apt-get install -y build-essential git python3-dev python3-pip
sudo apt-get install -y openjdk-11-jdk-headless android-sdk

# Install buildozer & dependencies
pip install buildozer cython

# Build APK
buildozer android debug

# Output: bin/mcqpaper-0.1-debug.apk
```

#### 2. Alternative: Use GitHub Actions

Create `.github/workflows/build-apk.yml` for automated builds:

```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Java
        uses: actions/setup-java@v2
        with:
          java-version: '11'
      - name: Build APK
        run: |
          pip install buildozer cython
          cd mobile_kivy
          buildozer android debug
      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: mcqpaper-debug.apk
          path: mobile_kivy/bin/mcqpaper-*.apk
```

### Build Configuration

The `buildozer.spec` includes:
- **Requirements**: `python3, kivy, pypdf2` (pure-Python libraries)
- **Permissions**: `READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET`
- **API Target**: Android 13 (API 33), min API 21
- **Architectures**: ARM64, ARMv7

### Deployment

1. **Debug APK** (testing):
   ```bash
   adb install -r bin/mcqpaper-0.1-debug.apk
   ```

2. **Release APK** (production, requires signing):
   ```bash
   buildozer android release
   # Sign with your keystore
   ```

## Running on Android

1. **Install APK**: Transfer to device or use `adb install`
2. **Grant Permissions**: Allow storage access on first run
3. **Add License**: App looks for `license.json` in app storage, or bundled with APK
4. **Load PDF**: Use "Add PDF (questions)" button on Export screen
5. **Generate Paper**: Fill form, click "Generate Random/Selected Paper"

## Features on Android

✓ Load PDF from device storage  
✓ Extract and display questions with checkboxes  
✓ Specify college, exam name, and date  
✓ Generate random question selections  
✓ Generate from manually selected questions  
✓ Save papers as .txt files to app storage  
✓ License validation on startup  
✓ Local question bank management (JSON storage)

## Troubleshooting

**Issue**: PyPDF2 not found on Android
- **Fix**: Ensure `pypdf2` is in `buildozer.spec` requirements and is pure-Python

**Issue**: Storage permissions denied
- **Fix**: Grant permissions via Android Settings > Apps > MCQ Paper Generator > Permissions

**Issue**: PDF text extraction empty
- **Fix**: Ensure PDF has extractable text (not image-based). Try a different PDF source.

## Future Enhancements

- DOCX/PDF generation on mobile (via `python-docx` + `reportlab`, requires testing)
- Server-side export service (generate DOCX→PDF on backend)
- Cloud sync for question banks
- Barcode/QR code for question IDs
