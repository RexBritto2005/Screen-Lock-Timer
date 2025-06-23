import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk, messagebox
import subprocess
import platform
import sys
import os

def background_timer_entry():
    import time
    import platform
    import subprocess
    import sys

    if len(sys.argv) < 3:
        sys.exit(1)
    try:
        total_seconds = int(sys.argv[2])
    except Exception:
        sys.exit(1)
    time.sleep(total_seconds)
    system = platform.system().lower()
    try:
        if system == "windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
        elif system == "darwin":
            subprocess.run([
                "/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"
            ], check=True)
        elif system == "linux":
            lock_commands = [
                ["gnome-screensaver-command", "--lock"],
                ["xdg-screensaver", "lock"],
                ["dm-tool", "lock"],
                ["loginctl", "lock-session"],
                ["xscreensaver-command", "-lock"]
            ]
            for cmd in lock_commands:
                try:
                    subprocess.run(cmd, check=True, timeout=5)
                    break
                except Exception:
                    continue
    except Exception:
        pass

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Lock Timer")
        self.root.geometry("435x280")
        self.root.resizable(False, False)
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, text="Screen Lock Timer",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        time_frame = ttk.LabelFrame(main_frame, text="Set Timer", padding="10")
        time_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))

        ttk.Label(time_frame, text="Minutes:").grid(row=0, column=0, padx=(0, 5))
        self.minutes_var = tk.StringVar(value="0")
        self.minutes_spinbox = ttk.Spinbox(time_frame, from_=0, to=999,
                                          textvariable=self.minutes_var, width=10)
        self.minutes_spinbox.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(time_frame, text="Seconds:").grid(row=0, column=2, padx=(0, 5))
        self.seconds_var = tk.StringVar(value="30")
        self.seconds_spinbox = ttk.Spinbox(time_frame, from_=0, to=59,
                                          textvariable=self.seconds_var, width=10)
        self.seconds_spinbox.grid(row=0, column=3)

        quick_frame = ttk.Frame(main_frame)
        quick_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))

        ttk.Label(quick_frame, text="Quick Set:").grid(row=0, column=0, padx=(0, 10))

        quick_times = [("5 min", 5, 0), ("10 min", 10, 0), ("30 min", 30, 0)]
        for i, (text, mins, secs) in enumerate(quick_times):
            btn = ttk.Button(quick_frame, text=text, width=8,
                           command=lambda m=mins, s=secs: self.set_quick_time(m, s))
            btn.grid(row=0, column=i+1, padx=2)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))

        self.start_button = ttk.Button(button_frame, text="Start Timer",
                                      command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=(0, 10))

    def set_quick_time(self, minutes, seconds):
        self.minutes_var.set(str(minutes))
        self.seconds_var.set(str(seconds))

    def start_timer(self):
        try:
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())

            if minutes == 0 and seconds == 0:
                messagebox.showerror("Error", "Please set a time greater than 0!")
                return

            total_seconds = minutes * 60 + seconds

            # --- DETACHED BACKGROUND PROCESS ---
            if getattr(sys, 'frozen', False):
                # Running as PyInstaller EXE
                exe_path = sys.executable
                args = [exe_path, "--background", str(total_seconds)]
            else:
                # Running as script
                python_exe = sys.executable
                script_path = os.path.abspath(__file__)
                args = [python_exe, script_path, "--background", str(total_seconds)]

            if platform.system().lower() == "windows":
                DETACHED_PROCESS = 0x00000008
                subprocess.Popen(
                    args,
                    creationflags=DETACHED_PROCESS,
                    close_fds=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                subprocess.Popen(
                    args,
                    start_new_session=True,
                    close_fds=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            # -----------------------------------

            self.root.after(100, self.root.destroy)  # Auto-close GUI after 100ms

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def on_window_close(self):
        self.root.destroy()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--background":
        background_timer_entry()
        return

    root = tb.Window(themename="cyborg")
    app = TimerApp(root)

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nTimer application closed.")

if __name__ == "__main__":
    main()