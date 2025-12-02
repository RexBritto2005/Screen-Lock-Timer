import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class ScreenLockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Locker")
        self.root.geometry("400x220")
        self.root.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Screen Locker", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Time input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Lock screen after:", font=("Arial", 10)).grid(row=0, column=0, columnspan=6, pady=5)
        
        # Hours
        tk.Label(input_frame, text="Hours:", font=("Arial", 9)).grid(row=1, column=0, padx=2)
        self.hours_entry = tk.Entry(input_frame, width=5, font=("Arial", 10))
        self.hours_entry.insert(0, "0")
        self.hours_entry.grid(row=1, column=1, padx=2)
        
        # Minutes
        tk.Label(input_frame, text="Minutes:", font=("Arial", 9)).grid(row=1, column=2, padx=2)
        self.minutes_entry = tk.Entry(input_frame, width=5, font=("Arial", 10))
        self.minutes_entry.insert(0, "5")
        self.minutes_entry.grid(row=1, column=3, padx=2)
        
        # Seconds
        tk.Label(input_frame, text="Seconds:", font=("Arial", 9)).grid(row=1, column=4, padx=2)
        self.seconds_entry = tk.Entry(input_frame, width=5, font=("Arial", 10))
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.grid(row=1, column=5, padx=2)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Timer not started", font=("Arial", 10), fg="gray")
        self.status_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Timer", command=self.start_timer, 
                                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                                       width=12, cursor="hand2")
        self.start_button.pack()
    
    def start_timer(self):
        try:
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)
            seconds = int(self.seconds_entry.get() or 0)
            
            if hours < 0 or minutes < 0 or seconds < 0:
                messagebox.showerror("Invalid Input", "Please enter positive numbers")
                return
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds == 0:
                messagebox.showerror("Invalid Input", "Please enter a time greater than 0")
                return
            
            # Get the path to lock_timer.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            lock_timer_path = os.path.join(script_dir, "lock_timer.py")
            
            # Start detached process
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                [sys.executable, lock_timer_path, str(total_seconds)],
                creationflags=DETACHED_PROCESS,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )
            
            self.status_label.config(text=f"Timer started! Screen will lock in {hours:02d}:{minutes:02d}:{seconds:02d}", fg="green")
            messagebox.showinfo("Timer Started", f"Screen will lock in {hours:02d}:{minutes:02d}:{seconds:02d}\nYou can close this window now.")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start timer: {str(e)}")

def main():
    root = tk.Tk()
    app = ScreenLockerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
