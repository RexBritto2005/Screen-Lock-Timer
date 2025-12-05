"""
Build script to create standalone executable
Run: python build_exe.py
"""
import PyInstaller.__main__
import shutil
from pathlib import Path

# Clean previous builds
for folder in ['build', 'dist']:
    if Path(folder).exists():
        shutil.rmtree(folder)

print("Building ScreenLocker.exe...")
print("This may take a few minutes...\n")

# Build executable
PyInstaller.__main__.run([
    'src/screen_locker_modern.py',
    '--name=ScreenLocker',
    '--onefile',
    '--windowed',
    '--noconsole',
    '--noconfirm',
])

print("\n✅ Build complete! Executable is in the 'dist' folder.")
print("Note: The exe file is standalone and can be moved anywhere.")
