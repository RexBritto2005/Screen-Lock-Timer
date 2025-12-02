# 🔒 Screen Locker

A minimal, sleek Windows application that automatically locks your screen after a specified time.

## ✨ Features

- **Pure Dark Theme** - Minimal black UI design
- **Two-Digit Time Format** - Professional HH:MM:SS display
- **Background Process** - Timer continues even after closing the window
- **Detached Execution** - Runs independently from the main application
- **Compact Design** - Small, efficient interface (380x280)

## 📦 Installation

Install required packages:
```bash
pip install -r requirements.txt
```

Or use the batch file:
```bash
install.bat
```

## 🚀 Usage

Run the application:
```bash
python run.py
```

## 🎨 Design

- **Pure Black Background** - True dark theme (#0a0a0a)
- **Minimal Interface** - No unnecessary elements
- **CustomTkinter** - Modern, native-looking widgets
- **Compact Layout** - Efficient use of space
- **Two-Digit Inputs** - Auto-formatting time fields

## 📁 Project Structure

```
ScreenLock/
├── src/
│   └── screen_locker_modern.py  # Main application
├── lock_timer.py                # Background timer process
├── run.py                       # Application launcher
├── install.bat                  # Windows installer
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

## 🔧 How It Works

1. Set hours, minutes, and seconds (two-digit format)
2. Click "Start" to begin the timer
3. A detached background process is created
4. Close the window anytime - timer keeps running
5. Screen locks automatically when time expires

## 💡 Technical Details

- Uses Windows API (`LockWorkStation`) for screen locking
- Detached subprocess ensures timer survives app closure
- CustomTkinter provides modern UI components
- Auto-formatting inputs to two-digit format
- Input validation and error handling

## 🎯 Requirements

- Python 3.7+
- Windows OS
- customtkinter 5.2.1+
- Pillow 10.1.0+

## 📝 Notes

- Timer runs independently in the background
- Safe to close the main window after starting
- Screen locks even if application is closed
- Fully detached operation
