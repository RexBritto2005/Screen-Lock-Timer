import customtkinter as ctk
import subprocess
import sys
import os
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernScreenLocker(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("")
        self.geometry("380x280")
        self.resizable(False, False)
        
        # Pure dark minimal color scheme
        self.bg_color = "#0a0a0a"
        self.card_bg = "#121212"
        self.input_bg = "#1a1a1a"
        self.accent_color = "#ffffff"
        self.accent_dim = "#666666"
        self.text_color = "#e0e0e0"
        
        self.configure(fg_color=self.bg_color)
        
        self.setup_ui()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Title - minimal
        title_label = ctk.CTkLabel(
            main_frame,
            text="Lock Timer",
            font=ctk.CTkFont(size=18, weight="normal"),
            text_color=self.text_color
        )
        title_label.pack(pady=(0, 20))
        
        # Time inputs container
        inputs_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        inputs_container.pack(pady=10)
        
        # Hours
        self.hours_var = ctk.StringVar(value="00")
        self.create_time_input(inputs_container, "Hours", self.hours_var, 0)
        
        # Separator
        sep1 = ctk.CTkLabel(
            inputs_container,
            text=":",
            font=ctk.CTkFont(size=24),
            text_color=self.accent_dim
        )
        sep1.grid(row=0, column=1, padx=5)
        
        # Minutes
        self.minutes_var = ctk.StringVar(value="05")
        self.create_time_input(inputs_container, "Minutes", self.minutes_var, 2)
        
        # Separator
        sep2 = ctk.CTkLabel(
            inputs_container,
            text=":",
            font=ctk.CTkFont(size=24),
            text_color=self.accent_dim
        )
        sep2.grid(row=0, column=3, padx=5)
        
        # Seconds
        self.seconds_var = ctk.StringVar(value="00")
        self.create_time_input(inputs_container, "Seconds", self.seconds_var, 4)
        
        # Status label - minimal
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.accent_dim
        )
        self.status_label.pack(pady=15)
        
        # Start button - minimal
        self.start_button = ctk.CTkButton(
            main_frame,
            text="Start",
            command=self.start_timer,
            font=ctk.CTkFont(size=13),
            fg_color=self.accent_color,
            hover_color=self.accent_dim,
            text_color=self.bg_color,
            height=40,
            width=180,
            corner_radius=4,
            border_width=0
        )
        self.start_button.pack(pady=5)
    
    def create_time_input(self, parent, label_text, variable, column):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=column)
        
        # Entry with validation
        entry = ctk.CTkEntry(
            container,
            textvariable=variable,
            width=55,
            height=55,
            font=ctk.CTkFont(size=28),
            fg_color=self.input_bg,
            border_color=self.input_bg,
            border_width=0,
            justify="center",
            text_color=self.text_color
        )
        entry.pack()
        
        # Bind to format as two digits
        entry.bind("<FocusOut>", lambda e: self.format_two_digits(variable))
        entry.bind("<KeyRelease>", lambda e: self.limit_input(variable, entry))
        
        # Label below
        label = ctk.CTkLabel(
            container,
            text=label_text,
            font=ctk.CTkFont(size=10),
            text_color=self.accent_dim
        )
        label.pack(pady=(4, 0))
    
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
            
            # Get the path to lock_timer.py
            script_dir = Path(__file__).parent.parent
            lock_timer_path = script_dir / "lock_timer.py"
            
            # Start detached process
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                [sys.executable, str(lock_timer_path), str(total_seconds)],
                creationflags=DETACHED_PROCESS,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )
            
            self.status_label.configure(
                text=f"Timer started · {hours:02d}:{minutes:02d}:{seconds:02d}",
                text_color=self.text_color
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
        dialog.configure(fg_color=self.bg_color)
        
        # Center dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Message
        msg_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=300,
            text_color=self.text_color
        )
        msg_label.pack(pady=50, padx=30)
        
        # OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            font=ctk.CTkFont(size=13),
            fg_color=self.accent_color,
            hover_color=self.accent_dim,
            text_color=self.bg_color,
            width=120,
            height=38,
            corner_radius=4
        )
        ok_button.pack(pady=10)

def main():
    app = ModernScreenLocker()
    app.mainloop()

if __name__ == "__main__":
    main()
