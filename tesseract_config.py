"""
Tesseract Configuration
Sets the Tesseract executable path for pytesseract
"""

import pytesseract
import os

# Common Tesseract installation paths on Windows
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Tesseract-OCR\tesseract.exe',
]

# Find Tesseract executable
tesseract_cmd = None
for path in TESSERACT_PATHS:
    if os.path.exists(path):
        tesseract_cmd = path
        break

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    print(f"✓ Tesseract configured: {tesseract_cmd}")
else:
    print("⚠ Tesseract not found in common locations. Please set manually:")
    print("  pytesseract.pytesseract.tesseract_cmd = r'C:\\Path\\To\\tesseract.exe'")
