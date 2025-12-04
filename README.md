# Screen Locker 🔒

Ever needed to step away from your computer but wanted it to lock automatically after a few minutes? This simple app does exactly that.

## What it does

Set a timer (hours, minutes, seconds), hit Start, and your Windows screen will lock when time's up. You can even close the app after starting the timer - it keeps running in the background.

## Quick Start

### Option 1: Use the standalone executable (easiest)
1. Download `ScreenLocker.exe` from the releases
2. Double-click and run
3. No installation needed!

### Option 2: Run from source
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python src/screen_locker_modern.py`

### Option 3: Build your own executable
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python build_exe.py` or just double-click `build.bat`
3. Find your exe in the `dist` folder

## How to use

1. Open the app
2. Set your timer (default is 5 minutes)
3. Click "Start"
4. Close the window if you want - timer keeps running
5. Your screen locks automatically when time's up

That's it. Simple.

## Why I made this

Sometimes you need to lock your screen after a delay - maybe you're downloading something, or waiting for a process to finish. Windows doesn't have a built-in timer for this, so here we are.

## Technical stuff

- Pure dark theme that's easy on the eyes
- Minimal design - no clutter
- Runs in the background after you start it
- Uses Windows' native lock function
- Built with Python and CustomTkinter

## Requirements

- Windows (uses Windows lock API)
- Python 3.7+ (if running from source)

## Files

- `src/screen_locker_modern.py` - Main app
- `lock_timer.py` - Background timer
- `build_exe.py` - Creates standalone executable
- `build.bat` - Easy build script for Windows

## Notes

The timer runs independently once started. Even if you close the app or it crashes, your screen will still lock at the scheduled time. This is by design - it's a feature, not a bug.
