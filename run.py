"""
Screen Locker Application Launcher
Run this file to start the modern screen locker
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from screen_locker_modern import main

if __name__ == "__main__":
    main()
