import customtkinter as ctk
import subprocess
import sys
import os
import ctypes
import threading
import time
from datetime import datetime, timedelta

ctk.set_appearance_mode("dark")

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
        self.geometry("420x480")
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
        
        # Title
        ctk.CTkLabel(main_frame, text="Screen Locker", font=ctk.CTkFont(size=18), 
                     text_color=self.TEXT).pack(pady=(0, 15))
        
        # Toggle switch frame
        toggle_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        toggle_frame.pack(pady=10)
        
        self.mode_label = ctk.CTkLabel(toggle_frame, text="Timer Mode", font=ctk.CTkFont(size=12), 
                                       text_color=self.ACCENT)
        self.mode_label.pack(side="left", padx=10)
        
        self.mode_switch = ctk.CTkSwitch(
            toggle_frame, 
            text="",
            command=self.toggle_mode,
            fg_color=self.INPUT_BG,
            progress_color=self.ACCENT,
            button_color=self.ACCENT,
            button_hover_color=self.ACCENT_DIM,
            width=50,
            height=25
        )
        self.mode_switch.pack(side="left")
        
        # Content frames
        self.timer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.specific_time_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        
        self.setup_timer_mode()
        self.setup_specific_time_mode()
        
        # Show timer mode by default
        self.timer_frame.pack(fill="both", expand=True)
        
        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=11), 
                                         text_color=self.ACCENT_DIM)
        self.status_label.pack(side="bottom", pady=10)
    
    def toggle_mode(self):
        # Smooth fade animation
        if self.mode_switch.get():
            # Switch to specific time mode
            self.animate_transition(self.timer_frame, self.specific_time_frame)
            self.mode_label.configure(text="Specific Time Mode")
        else:
            # Switch to timer mode
            self.animate_transition(self.specific_time_frame, self.timer_frame)
            self.mode_label.configure(text="Timer Mode")
    
    def animate_transition(self, old_frame, new_frame):
        """Smooth transition between frames"""
        old_frame.pack_forget()
        new_frame.pack(fill="both", expand=True)
        # Trigger update to ensure smooth transition
        self.update_idletasks()
    
    def setup_timer_mode(self):
        
        inputs = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        inputs.pack(pady=20)
        
        self.hours_var = ctk.StringVar(value="00")
        self.minutes_var = ctk.StringVar(value="05")
        self.seconds_var = ctk.StringVar(value="00")
        
        for i, (label, var) in enumerate([("Hours", self.hours_var), ("Minutes", self.minutes_var), ("Seconds", self.seconds_var)]):
            self.create_time_input(inputs, label, var, i * 2)
            if i < 2:
                ctk.CTkLabel(inputs, text=":", font=ctk.CTkFont(size=24), 
                           text_color=self.ACCENT_DIM).grid(row=0, column=i * 2 + 1, padx=5)
        
        # Quick setup buttons
        quick_frame = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        quick_frame.pack(pady=15)
        
        quick_buttons = [
            ("10s", 0, 0, 10),
            ("1m", 0, 1, 0),
            ("1h", 1, 0, 0)
        ]
        
        for text, hours, minutes, seconds in quick_buttons:
            ctk.CTkButton(
                quick_frame, text=text, 
                command=lambda h=hours, m=minutes, s=seconds: self.set_quick_time(h, m, s),
                font=ctk.CTkFont(size=11), fg_color=self.INPUT_BG, 
                hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                height=28, width=60, corner_radius=4, border_width=0
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(self.timer_frame, text="Start", command=self.start_timer, font=ctk.CTkFont(size=13),
                     fg_color=self.ACCENT, hover_color=self.ACCENT_DIM, text_color=self.BG_COLOR,
                     height=40, width=180, corner_radius=4, border_width=0).pack(pady=20)
    
    def setup_specific_time_mode(self):
        
        # Time input frame
        time_input_frame = ctk.CTkFrame(self.specific_time_frame, fg_color="transparent")
        time_input_frame.pack(pady=30)
        
        # Hour input
        self.lock_hour_var = ctk.StringVar(value="10")
        hour_container = ctk.CTkFrame(time_input_frame, fg_color="transparent")
        hour_container.grid(row=0, column=0, padx=5)
        
        # Up arrow
        ctk.CTkButton(hour_container, text="▲", width=55, height=20,
                     font=ctk.CTkFont(size=12), fg_color=self.INPUT_BG,
                     hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                     corner_radius=4, border_width=0,
                     command=lambda: self.increment_specific_time(self.lock_hour_var, 23)).pack()
        
        hour_entry = ctk.CTkEntry(hour_container, textvariable=self.lock_hour_var, width=55, height=55,
                                 font=ctk.CTkFont(size=28), fg_color=self.INPUT_BG,
                                 border_width=0, justify="center", text_color=self.TEXT)
        hour_entry.pack(pady=2)
        hour_entry.bind("<FocusOut>", lambda e: self.format_two_digits(self.lock_hour_var))
        hour_entry.bind("<KeyRelease>", lambda e: self.limit_hour_input(self.lock_hour_var, hour_entry))
        
        # Down arrow
        ctk.CTkButton(hour_container, text="▼", width=55, height=20,
                     font=ctk.CTkFont(size=12), fg_color=self.INPUT_BG,
                     hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                     corner_radius=4, border_width=0,
                     command=lambda: self.decrement_specific_time(self.lock_hour_var, 23)).pack()
        
        ctk.CTkLabel(hour_container, text="Hour", font=ctk.CTkFont(size=10),
                    text_color=self.ACCENT_DIM).pack(pady=(4, 0))
        
        # Colon separator
        ctk.CTkLabel(time_input_frame, text=":", font=ctk.CTkFont(size=24), 
                    text_color=self.ACCENT_DIM).grid(row=0, column=1, padx=5)
        
        # Minute input
        self.lock_minute_var = ctk.StringVar(value="30")
        minute_container = ctk.CTkFrame(time_input_frame, fg_color="transparent")
        minute_container.grid(row=0, column=2, padx=5)
        
        # Up arrow
        ctk.CTkButton(minute_container, text="▲", width=55, height=20,
                     font=ctk.CTkFont(size=12), fg_color=self.INPUT_BG,
                     hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                     corner_radius=4, border_width=0,
                     command=lambda: self.increment_specific_time(self.lock_minute_var, 59)).pack()
        
        minute_entry = ctk.CTkEntry(minute_container, textvariable=self.lock_minute_var, width=55, height=55,
                                   font=ctk.CTkFont(size=28), fg_color=self.INPUT_BG,
                                   border_width=0, justify="center", text_color=self.TEXT)
        minute_entry.pack(pady=2)
        minute_entry.bind("<FocusOut>", lambda e: self.format_two_digits(self.lock_minute_var))
        minute_entry.bind("<KeyRelease>", lambda e: self.limit_minute_input(self.lock_minute_var, minute_entry))
        
        # Down arrow
        ctk.CTkButton(minute_container, text="▼", width=55, height=20,
                     font=ctk.CTkFont(size=12), fg_color=self.INPUT_BG,
                     hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                     corner_radius=4, border_width=0,
                     command=lambda: self.decrement_specific_time(self.lock_minute_var, 59)).pack()
        
        ctk.CTkLabel(minute_container, text="Minute", font=ctk.CTkFont(size=10),
                    text_color=self.ACCENT_DIM).pack(pady=(4, 0))
        
        # Info text
        ctk.CTkLabel(self.specific_time_frame, text="24-hour format (e.g., 14:30 for 2:30 PM)", 
                    font=ctk.CTkFont(size=10), text_color=self.ACCENT_DIM).pack(pady=10)
        
        # Start button
        ctk.CTkButton(self.specific_time_frame, text="Start", command=self.lock_at_time, 
                     font=ctk.CTkFont(size=13),
                     fg_color=self.ACCENT, hover_color=self.ACCENT_DIM, text_color=self.BG_COLOR,
                     height=40, width=180, corner_radius=4, border_width=0).pack(pady=20)
    
    def create_time_input(self, parent, label_text, variable, column):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=column)
        
        # Up arrow button
        up_btn = ctk.CTkButton(container, text="▲", width=55, height=20,
                              font=ctk.CTkFont(size=12), fg_color=self.INPUT_BG,
                              hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                              corner_radius=4, border_width=0,
                              command=lambda: self.increment_time(variable, label_text))
        up_btn.pack()
        
        entry = ctk.CTkEntry(container, textvariable=variable, width=55, height=55,
                            font=ctk.CTkFont(size=28), fg_color=self.INPUT_BG,
                            border_width=0, justify="center", text_color=self.TEXT)
        entry.pack(pady=2)
        entry.bind("<FocusOut>", lambda e: self.format_two_digits(variable))
        entry.bind("<KeyRelease>", lambda e: self.limit_input(variable, entry))
        
        # Down arrow button
        down_btn = ctk.CTkButton(container, text="▼", width=55, height=20,
                                font=ctk.CTkFont(size=12), fg_color=self.INPUT_BG,
                                hover_color=self.ACCENT_DIM, text_color=self.TEXT,
                                corner_radius=4, border_width=0,
                                command=lambda: self.decrement_time(variable, label_text))
        down_btn.pack()
        
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
    
    def set_quick_time(self, hours, minutes, seconds):
        self.hours_var.set(f"{hours:02d}")
        self.minutes_var.set(f"{minutes:02d}")
        self.seconds_var.set(f"{seconds:02d}")
    
    def increment_time(self, variable, label):
        try:
            value = int(variable.get() or 0)
            if label == "Hours":
                value = (value + 1) % 100
            elif label == "Minutes" or label == "Seconds":
                value = (value + 1) % 60
            variable.set(f"{value:02d}")
        except ValueError:
            variable.set("00")
    
    def decrement_time(self, variable, label):
        try:
            value = int(variable.get() or 0)
            if label == "Hours":
                value = (value - 1) % 100
            elif label == "Minutes" or label == "Seconds":
                value = (value - 1) % 60
            variable.set(f"{value:02d}")
        except ValueError:
            variable.set("00")
    
    def increment_specific_time(self, variable, max_val):
        try:
            value = int(variable.get() or 0)
            value = (value + 1) % (max_val + 1)
            variable.set(f"{value:02d}")
        except ValueError:
            variable.set("00")
    
    def decrement_specific_time(self, variable, max_val):
        try:
            value = int(variable.get() or 0)
            value = (value - 1) % (max_val + 1)
            variable.set(f"{value:02d}")
        except ValueError:
            variable.set("00")
    
    def limit_hour_input(self, var, entry):
        value = var.get()
        if len(value) > 2:
            var.set(value[:2])
            entry.icursor(2)
        # Validate hour (0-23)
        try:
            if value and int(value) > 23:
                var.set("23")
        except ValueError:
            pass
    
    def limit_minute_input(self, var, entry):
        value = var.get()
        if len(value) > 2:
            var.set(value[:2])
            entry.icursor(2)
        # Validate minute (0-59)
        try:
            if value and int(value) > 59:
                var.set("59")
        except ValueError:
            pass
    
    def lock_at_time(self):
        try:
            target_hours = int(self.lock_hour_var.get() or 0)
            target_mins = int(self.lock_minute_var.get() or 0)
            
            if target_hours < 0 or target_hours > 23:
                self.show_message("Invalid Input", "Hour must be between 0 and 23", error=True)
                return
            
            if target_mins < 0 or target_mins > 59:
                self.show_message("Invalid Input", "Minute must be between 0 and 59", error=True)
                return
            
            now = datetime.now()
            target_time = now.replace(hour=target_hours, minute=target_mins, second=0, microsecond=0)
            
            # If target time is in the past, set it for tomorrow
            if target_time <= now:
                target_time += timedelta(days=1)
                day_text = "tomorrow"
            else:
                day_text = "today"
            
            seconds_until = int((target_time - now).total_seconds())
            
            # Start background thread
            timer_thread = threading.Thread(
                target=self.lock_screen_after_delay, 
                args=(seconds_until,),
                daemon=False
            )
            timer_thread.start()
            
            self.status_label.configure(
                text=f"Will lock at {target_hours:02d}:{target_mins:02d} {day_text}",
                text_color=self.TEXT
            )
            self.show_message(
                "Lock Scheduled",
                f"Screen will lock at {target_hours:02d}:{target_mins:02d} {day_text}\n\nYou can close this window."
            )
            
        except ValueError:
            self.show_message("Invalid Input", "Please enter valid time", error=True)
        except Exception as e:
            self.show_message("Error", f"Failed to schedule lock: {str(e)}", error=True)
    
    def lock_screen_after_delay(self, total_seconds):
        """Background thread to lock screen after delay"""
        time.sleep(total_seconds)
        ctypes.windll.user32.LockWorkStation()
    
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
            
            # Start background thread (daemon=False so it continues after window closes)
            timer_thread = threading.Thread(
                target=self.lock_screen_after_delay, 
                args=(total_seconds,),
                daemon=False
            )
            timer_thread.start()
            
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
