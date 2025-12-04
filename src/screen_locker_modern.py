import customtkinter as ctk
import subprocess
import sys
import os
import tempfile
from pathlib import Path

ctk.set_appearance_mode("dark")

# Embedded lock timer script
LOCK_TIMER_SCRIPT = """import sys
import time
import ctypes

if __name__ == "__main__":
    total_seconds = int(sys.argv[1])
    time.sleep(total_seconds)
    ctypes.windll.user32.LockWorkStation()
"""

class ModernScreenLocker(ctk.CTk):
    # Color constants
    BG_COLOR = "#0a0a0a"
    INPUT_BG = "#1a1a1a"
    ACCENT = "#ffffff"
    ACCENT_DIM = "#666666"
    TEXT = "#e0e0e0"
    
    def __init__(self):
        super().__init__()
        self.title("")
        self.geometry("380x280")
        self.resizable(False, False)
        self.configure(fg_color=self.BG_COLOR)
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f'+{x}+{y}')
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        ctk.CTkLabel(main_frame, text="Lock Timer", font=ctk.CTkFont(size=18), 
                     text_color=self.TEXT).pack(pady=(0, 20))
        
        inputs = ctk.CTkFrame(main_frame, fg_color="transparent")
        inputs.pack(pady=10)
        
        self.hours_var = ctk.StringVar(value="00")
        self.minutes_var = ctk.StringVar(value="05")
        self.seconds_var = ctk.StringVar(value="00")
        
        for i, (label, var) in enumerate([("Hours", self.hours_var), ("Minutes", self.minutes_var), ("Seconds", self.seconds_var)]):
            self.create_time_input(inputs, label, var, i * 2)
            if i < 2:
                ctk.CTkLabel(inputs, text=":", font=ctk.CTkFont(size=24), 
                           text_color=self.ACCENT_DIM).grid(row=0, column=i * 2 + 1, padx=5)
        
        self.status_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=11), 
                                         text_color=self.ACCENT_DIM)
        self.status_label.pack(pady=15)
        
        ctk.CTkButton(main_frame, text="Start", command=self.start_timer, font=ctk.CTkFont(size=13),
                     fg_color=self.ACCENT, hover_color=self.ACCENT_DIM, text_color=self.BG_COLOR,
                     height=40, width=180, corner_radius=4, border_width=0).pack(pady=5)
    
    def create_time_input(self, parent, label_text, variable, column):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=column)
        
        entry = ctk.CTkEntry(container, textvariable=variable, width=55, height=55,
                            font=ctk.CTkFont(size=28), fg_color=self.INPUT_BG,
                            border_width=0, justify="center", text_color=self.TEXT)
        entry.pack()
        entry.bind("<FocusOut>", lambda e: self.format_two_digits(variable))
        entry.bind("<KeyRelease>", lambda e: self.limit_input(variable, entry))
        
        ctk.CTkLabel(container, text=label_text, font=ctk.CTkFont(size=10),
                    text_color=self.ACCENT_DIM).pack(pady=(4, 0))
    
    def format_two_digits(self, var):
        try:
            value = int(var.get() or 0)
            var.set(f"{value:02d}")
        except ValueError:
            var.set("00")
    
    def limit_input(self, var, entry):
        value = var.get()
        if len(value) > 2:
            var.set(value[:2])
            entry.icursor(2)
    
    def start_timer(self):
        try:
            hours = int(self.hours_var.get() or 0)
            minutes = int(self.minutes_var.get() or 0)
            seconds = int(self.seconds_var.get() or 0)
            
            if hours < 0 or minutes < 0 or seconds < 0:
                self.show_message("Invalid Input", "Please enter positive numbers", error=True)
                return
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds == 0:
                self.show_message("Invalid Input", "Please enter a time greater than 0", error=True)
                return
            
            # Create temporary lock timer script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(LOCK_TIMER_SCRIPT)
                temp_script = f.name
            
            # Start detached process
            DETACHED_PROCESS = 0x00000008
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(
                [sys.executable, temp_script, str(total_seconds)],
                creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )
            
            self.status_label.configure(
                text=f"Timer started · {hours:02d}:{minutes:02d}:{seconds:02d}",
                text_color=self.TEXT
            )
            self.show_message(
                "Timer Started",
                f"Screen will lock in {hours:02d}:{minutes:02d}:{seconds:02d}\n\nYou can close this window."
            )
            
        except ValueError:
            self.show_message("Invalid Input", "Please enter valid numbers", error=True)
        except Exception as e:
            self.show_message("Error", f"Failed to start timer: {str(e)}", error=True)
    
    def show_message(self, title, message, error=False):
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("350x200")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=13), wraplength=300,
                    text_color=self.TEXT).pack(pady=50, padx=30)
        
        ctk.CTkButton(dialog, text="OK", command=dialog.destroy, font=ctk.CTkFont(size=13),
                     fg_color=self.ACCENT, hover_color=self.ACCENT_DIM, text_color=self.BG_COLOR,
                     width=120, height=38, corner_radius=4).pack(pady=10)

def main():
    app = ModernScreenLocker()
    app.mainloop()

if __name__ == "__main__":
    main()
