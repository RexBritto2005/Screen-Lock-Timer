import sys
import time
import ctypes

def lock_screen():
    ctypes.windll.user32.LockWorkStation()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: lock_timer.py <seconds>")
        sys.exit(1)
    
    total_seconds = int(sys.argv[1])
    time.sleep(total_seconds)
    lock_screen()
