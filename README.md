<p align="center">
  <img src="icon.ico" height="100" alt="App Icon" />
</p>

<h1 align="center">🔐 ScreenLockTimer</h1>

<p align="center">
  A cross-platform screen lock timer app built with Python and ttkbootstrap.<br>
  Schedule a time, walk away, and your screen locks automatically.
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square" alt="Python">
  </a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-success?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/badge/GUI-ttkbootstrap%20%7C%20Tkinter-orange?style=flat-square" alt="GUI">
  <img src="https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square" alt="Version">
</p>

---

## ✨ Features

- ⏲️ Set custom countdown time in minutes and seconds
- 🔘 Quick Set buttons (5, 10, 30 minutes)
- 🛡️ Locks screen automatically in the background
- 🎨 Beautiful dark UI using `ttkbootstrap`'s *Cyborg* theme
- 💻 Cross-platform locking:
  - **Windows** – `rundll32.exe user32.dll,LockWorkStation`
  - **macOS** – `CGSession -suspend`
  - **Linux** – Tries multiple screen locker commands

---

## 📥 Download

<p align="center">
  👉 <a href="https://github.com/YOUR_USERNAME/ScreenLockTimer/releases/latest"><b>Download the latest Windows EXE</b></a><br>
  No Python required — just run it!
</p>

> 📝 On first launch, Windows SmartScreen may require you to click “More Info” → “Run Anyway”.

---

### 🛠️ Build Your Own Executable (EXE)

If you'd rather build the `.exe` yourself using PyInstaller:

### ✅ Prerequisites:

- Python 3.9+
- `ttkbootstrap` package installed
- `PyInstaller` installed

### ✅ Step 1: Install dependencies

```bash
pip install ttkbootstrap pyinstaller
```

### ✅ Step 2: Run the build command

```bash
pyinstaller --noconsole --onefile --icon=icon.ico ScreenLock.py
```

### ✅ Step 3: Locate your executable

After building, your executable will be located in the dist/ folder:

---

### 🧑‍💻 Run from Source (Python)

```bash
git clone https://github.com/RexBritto2005/Screen-Lock-Timer.git
cd ScreenLockTimer
pip install ttkbootstrap
python ScreenLock.py
```
