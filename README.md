# Screen Locker Application

A simple Windows application that locks your screen after a specified time period.

## Features

- Set custom timer in minutes
- Visual countdown display
- Start/Stop timer controls
- Automatically locks Windows screen when timer expires

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- Windows OS

## Usage

1. Run the application:
   ```
   python screen_locker.py
   ```

2. Enter the number of minutes before the screen should lock

3. Click "Start Timer" to begin the countdown

4. Click "Stop Timer" to cancel the lock

## How It Works

The application uses Windows API (`LockWorkStation`) to lock the screen when the timer expires. The countdown runs in a separate thread to keep the UI responsive.
