import tkinter as tk
from tkinter import ttk
import time
import threading
 
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Timer")
        self.root.configure(bg="#808080")
        
        self.timers = []
        for i in range(2):
            for j in range(2):
                frame = tk.Frame(root, bg="#808080", bd=2, relief="groove")
                frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                timer = self.create_timer(frame, f"Timer {i*2 + j + 1}")
                self.timers.append(timer)
        
        for i in range(2):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i, weight=1)
 
    def create_timer(self, parent, name):
        timer_data = {}  
        
        timer_frame = tk.Frame(parent, bg="#808080")
        timer_frame.pack(expand=True, fill="both", padx=5, pady=5)
 
        label = tk.Label(timer_frame, text=name, font=("Arial", 12), bg="#808080", fg="black")
        label.pack(pady=5)
 
        top_frame = tk.Frame(timer_frame, bg="#808080")
        top_frame.pack(fill="x", pady=5)
 
        for mins in [5, 15, 35]:
            btn = tk.Button(
                top_frame, 
                text=f"{mins} min", 
                command=lambda m=mins, td=timer_data: self.set_time(td, m * 60),
                bg="#4CAF50",
                fg="black",
                relief="flat"
            )
            btn.pack(side="left", expand=True, padx=2)
 
        mid_frame = tk.Frame(timer_frame, bg="#808080")
        mid_frame.pack(fill="x", pady=5)
 
        time_var = tk.StringVar(value="00:05:00")
        time_entry = tk.Entry(
            mid_frame, 
            textvariable=time_var, 
            font=("Arial", 14), 
            justify="center",
            bg="#FFFFFF",
            relief="flat"
        )
        time_entry.pack(fill="x", padx=10)
 
        bottom_frame = tk.Frame(timer_frame, bg="#808080")
        bottom_frame.pack(fill="x", pady=5)
 
        start_btn = tk.Button(
            bottom_frame, 
            text="Start", 
            command=lambda td=timer_data: self.start_timer(td),
            bg="#4CAF50",
            fg="black",
            relief="flat"
        )
        start_btn.pack(side="left", expand=True, padx=2)
 
        reset_btn = tk.Button(
            bottom_frame, 
            text="Reset", 
            command=lambda td=timer_data: self.reset_timer(td),
            bg="#4CAF50",
            fg="black",
            relief="flat"
        )
        reset_btn.pack(side="left", expand=True, padx=2)
 
        alert_btn = tk.Button(
            timer_frame, 
            text="TIME'S UP!", 
            bg="#4CAF50",
            fg="black",
            relief="flat"
        )
        alert_btn.pack(fill="x", padx=10, pady=5)
        alert_btn.pack_forget()
 
        timer_data.update({
            "frame": timer_frame,
            "time_var": time_var,
            "alert_btn": alert_btn,
            "running": False,
            "remaining": 0,
            "flash_count": 0
        })
        
        return timer_data
 
    def set_time(self, timer_data, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        timer_data["time_var"].set(f"{hours:02d}:{mins:02d}:{secs:02d}")
 
    def start_timer(self, timer_data):
        if not timer_data["running"]:
            timer_data["running"] = True
            timer_data["remaining"] = self.parse_time(timer_data["time_var"].get())
            self.update_timer(timer_data)
 
    def reset_timer(self, timer_data):
        timer_data["running"] = False
        timer_data["alert_btn"].pack_forget()
        self.set_time(timer_data, 300)
 
    def parse_time(self, time_str):
        h, m, s = map(int, time_str.split(":"))
        return h * 3600 + m * 60 + s
 
    def update_timer(self, timer_data):
        if timer_data["running"] and timer_data["remaining"] > 0:
            timer_data["remaining"] -= 1
            self.set_time(timer_data, timer_data["remaining"])
            self.root.after(1000, lambda: self.update_timer(timer_data))
        elif timer_data["remaining"] == 0 and timer_data["running"]:
            timer_data["running"] = False
            timer_data["alert_btn"].pack(fill="x", padx=10, pady=5)
            self.flash_alert(timer_data)
 
    def flash_alert(self, timer_data):
        current_color = timer_data["alert_btn"].cget("bg")
        new_color = "#808080" if current_color == "#4CAF50" else "#4CAF50"
        timer_data["alert_btn"].config(bg=new_color)
        if timer_data["flash_count"] < 10:
            timer_data["flash_count"] += 1
            self.root.after(500, lambda: self.flash_alert(timer_data))
        else:
            timer_data["flash_count"] = 0
            timer_data["alert_btn"].pack_forget()
 
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = TimerApp(root)
    root.mainloop()
