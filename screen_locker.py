import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import threading
import time

class ScreenLockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Locker")
        self.root.geometry("350x200")
        self.root.resizable(False, False)
        
        self.timer_thread = None
        self.is_running = False
        self.remaining_time = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Screen Locker", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Time input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Lock screen after:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        
        self.time_entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.time_entry.insert(0, "5")
        self.time_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="minutes", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Timer not started", font=("Arial", 10), fg="gray")
        self.status_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Timer", command=self.start_timer, 
                                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                                       width=12, cursor="hand2")
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Timer", command=self.stop_timer, 
                                      bg="#f44336", fg="white", font=("Arial", 10, "bold"), 
                                      width=12, cursor="hand2", state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
    
    def start_timer(self):
        try:
            minutes = float(self.time_entry.get())
            if minutes <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive number")
                return
            
            self.remaining_time = int(minutes * 60)
            self.is_running = True
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.time_entry.config(state=tk.DISABLED)
            
            self.timer_thread = threading.Thread(target=self.countdown, daemon=True)
            self.timer_thread.start()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def countdown(self):
        while self.is_running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.status_label.config(text=f"Locking in: {mins:02d}:{secs:02d}", fg="blue")
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.is_running and self.remaining_time == 0:
            self.lock_screen()
            self.reset_ui()
    
    def stop_timer(self):
        self.is_running = False
        self.reset_ui()
    
    def reset_ui(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.time_entry.config(state=tk.NORMAL)
        self.status_label.config(text="Timer not started", fg="gray")
        self.remaining_time = 0
    
    def lock_screen(self):
        # Lock the Windows screen
        ctypes.windll.user32.LockWorkStation()

def main():
    root = tk.Tk()
    app = ScreenLockerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
