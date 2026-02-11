#!/usr/bin/env python3
import tkinter as tk
from tkinter import font as tkfont
import serial
import threading
import time
from datetime import datetime

class RailwayAxleCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Axle Counter System")
        
        # For 3.5" TFT (480x320)
        self.root.geometry("480x320")
        self.root.configure(bg='#1a1a2e')
        
        # Variables
        self.axle_count = 0
        self.target_count = 0
        self.temperature = 0.0
        self.compare_mode = False
        self.match_status = False
        self.hot_axle = False
        
        # Serial ports
        self.uno_serial = None
        self.nano_serial = None
        self.serial_lock = threading.Lock()
        
        # Setup GUI
        self.setup_gui()
        
        # Connect to Arduinos
        self.connect_arduinos()
        
        # Start serial reader threads
        self.running = True
        self.start_serial_threads()
        
    def setup_gui(self):
        # Title Bar
        title_frame = tk.Frame(self.root, bg='#0f3460', height=40)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🚂 RAILWAY AXLE COUNTER",
            font=('Arial', 16, 'bold'),
            bg='#0f3460',
            fg='#ffffff'
        )
        title_label.pack(pady=5)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left Panel - Counters
        left_frame = tk.Frame(main_frame, bg='#1a1a2e')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Axle Count Display
        count_frame = tk.Frame(left_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        count_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            count_frame,
            text="AXLE COUNT",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#e94560'
        ).pack()
        
        self.count_label = tk.Label(
            count_frame,
            text="00",
            font=('Arial', 48, 'bold'),
            bg='#16213e',
            fg='#00ff00'
        )
        self.count_label.pack(pady=10)
        
        # Target Display
        target_frame = tk.Frame(left_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        target_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            target_frame,
            text="TARGET",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#e94560'
        ).pack()
        
        self.target_label = tk.Label(
            target_frame,
            text="00",
            font=('Arial', 36, 'bold'),
            bg='#16213e',
            fg='#ffaa00'
        )
        self.target_label.pack(pady=5)
        
        # Right Panel - Controls
        right_frame = tk.Frame(main_frame, bg='#1a1a2e')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        
        # Temperature Display
        temp_frame = tk.Frame(right_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        temp_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            temp_frame,
            text="🌡️ AXLE TEMP",
            font=('Arial', 11, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack()
        
        self.temp_label = tk.Label(
            temp_frame,
            text="--°C",
            font=('Arial', 24, 'bold'),
            bg='#16213e',
            fg='#00aaff'
        )
        self.temp_label.pack(pady=5)
        
        self.hot_axle_label = tk.Label(
            temp_frame,
            text="",
            font=('Arial', 10, 'bold'),
            bg='#16213e',
            fg='#ff0000'
        )
        self.hot_axle_label.pack()
        
        # Mode Toggle
        mode_frame = tk.Frame(right_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        mode_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            mode_frame,
            text="MODE",
            font=('Arial', 11, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        ).pack()
        
        self.mode_button = tk.Button(
            mode_frame,
            text="COUNT",
            font=('Arial', 12, 'bold'),
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#e94560',
            command=self.toggle_mode,
            width=10
        )
        self.mode_button.pack(pady=5)
        
        # Match Indicator
        self.match_label = tk.Label(
            right_frame,
            text="",
            font=('Arial', 14, 'bold'),
            bg='#1a1a2e',
            fg='#00ff00'
        )
        self.match_label.pack(pady=5)
        
        # Bottom Panel - Target Entry
        bottom_frame = tk.Frame(self.root, bg='#0f3460')
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Target entry
        entry_frame = tk.Frame(bottom_frame, bg='#0f3460')
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            entry_frame,
            text="Set Target:",
            font=('Arial', 10, 'bold'),
            bg='#0f3460',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.target_entry = tk.Entry(
            entry_frame,
            font=('Arial', 14),
            width=5,
            bg='#ffffff',
            fg='#000000'
        )
        self.target_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            entry_frame,
            text="SET",
            font=('Arial', 10, 'bold'),
            bg='#e94560',
            fg='#ffffff',
            command=self.set_target,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        # Reset button
        tk.Button(
            bottom_frame,
            text="RESET",
            font=('Arial', 10, 'bold'),
            bg='#ff6b6b',
            fg='#ffffff',
            command=self.reset_count,
            width=8
        ).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Initializing...",
            font=('Arial', 8),
            bg='#0f3460',
            fg='#aaaaaa',
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
        
    def connect_arduinos(self):
        try:
            # Try to connect to UNO (usually /dev/ttyUSB0 or /dev/ttyACM0)
            self.uno_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            self.update_status("UNO connected on /dev/ttyUSB0")
        except:
            try:
                self.uno_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
                time.sleep(2)
                self.update_status("UNO connected on /dev/ttyACM0")
            except Exception as e:
                self.update_status(f"UNO connection failed: {e}")
        
        try:
            # Try to connect to Nano
            self.nano_serial = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
            time.sleep(2)
            self.update_status("Nano connected on /dev/ttyUSB1")
        except:
            try:
                self.nano_serial = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
                time.sleep(2)
                self.update_status("Nano connected on /dev/ttyACM1")
            except Exception as e:
                self.update_status(f"Nano connection failed: {e}")
    
    def start_serial_threads(self):
        if self.uno_serial:
            uno_thread = threading.Thread(target=self.read_uno_serial, daemon=True)
            uno_thread.start()
        
        if self.nano_serial:
            nano_thread = threading.Thread(target=self.read_nano_serial, daemon=True)
            nano_thread.start()
    
    def read_uno_serial(self):
        while self.running:
            try:
                if self.uno_serial and self.uno_serial.in_waiting:
                    line = self.uno_serial.readline().decode('utf-8').strip()
                    self.process_uno_message(line)
            except Exception as e:
                print(f"UNO read error: {e}")
            time.sleep(0.01)
    
    def read_nano_serial(self):
        while self.running:
            try:
                if self.nano_serial and self.nano_serial.in_waiting:
                    line = self.nano_serial.readline().decode('utf-8').strip()
                    self.process_nano_message(line)
            except Exception as e:
                print(f"Nano read error: {e}")
            time.sleep(0.01)
    
    def process_uno_message(self, msg):
        if msg.startswith("COUNT:"):
            self.axle_count = int(msg.split(":")[1])
            self.update_count_display()
        elif msg.startswith("MATCH:"):
            self.match_status = (msg.split(":")[1] == "TRUE")
            self.update_match_display()
        elif msg == "UNO_READY":
            self.update_status("UNO Ready")
    
    def process_nano_message(self, msg):
        if msg.startswith("TEMP:"):
            self.temperature = float(msg.split(":")[1])
            self.update_temp_display()
        elif msg == "HOT_AXLE_ALERT":
            self.hot_axle = True
            self.update_temp_display()
        elif msg == "NANO_READY":
            self.update_status("Nano Ready")
    
    def update_count_display(self):
        self.count_label.config(text=f"{self.axle_count:02d}")
        
        # Color code based on comparison
        if self.compare_mode and self.target_count > 0:
            if self.axle_count == self.target_count:
                self.count_label.config(fg='#00ff00')  # Green = match
            elif self.axle_count > self.target_count:
                self.count_label.config(fg='#ff0000')  # Red = exceeded
            else:
                self.count_label.config(fg='#ffaa00')  # Yellow = counting
        else:
            self.count_label.config(fg='#00ff00')  # Green = normal count
    
    def update_temp_display(self):
        if self.temperature > -50:  # Valid reading
            self.temp_label.config(text=f"{self.temperature:.1f}°C")
            
            # Color code by temperature
            if self.temperature > 80:
                self.temp_label.config(fg='#ff0000')
                self.hot_axle_label.config(text="⚠️ HOT AXLE!")
            elif self.temperature > 60:
                self.temp_label.config(fg='#ffaa00')
                self.hot_axle_label.config(text="Warning")
            else:
                self.temp_label.config(fg='#00aaff')
                self.hot_axle_label.config(text="Normal")
        else:
            self.temp_label.config(text="--°C")
            self.hot_axle_label.config(text="No sensor")
    
    def update_match_display(self):
        if self.match_status and self.compare_mode:
            self.match_label.config(text="✓ MATCH!", fg='#00ff00')
        else:
            self.match_label.config(text="")
    
    def toggle_mode(self):
        self.compare_mode = not self.compare_mode
        
        if self.compare_mode:
            self.mode_button.config(text="COMPARE", bg='#e94560')
            self.send_to_uno("MODE:COMPARE\n")
        else:
            self.mode_button.config(text="COUNT", bg='#0f3460')
            self.send_to_uno("MODE:COUNT\n")
            self.match_label.config(text="")
    
    def set_target(self):
        try:
            target = int(self.target_entry.get())
            if 0 <= target <= 99:
                self.target_count = target
                self.target_label.config(text=f"{target:02d}")
                self.send_to_uno(f"TARGET:{target}\n")
                self.update_status(f"Target set to {target}")
                self.target_entry.delete(0, tk.END)
            else:
                self.update_status("Target must be 0-99")
        except ValueError:
            self.update_status("Invalid target number")
    
    def reset_count(self):
        self.send_to_uno("RESET\n")
        self.axle_count = 0
        self.update_count_display()
        self.match_label.config(text="")
        self.update_status("Count reset")
    
    def send_to_uno(self, message):
        try:
            if self.uno_serial:
                with self.serial_lock:
                    self.uno_serial.write(message.encode())
        except Exception as e:
            self.update_status(f"UNO send error: {e}")
    
    def update_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"[{timestamp}] {message}")
    
    def on_closing(self):
        self.running = False
        if self.uno_serial:
            self.uno_serial.close()
        if self.nano_serial:
            self.nano_serial.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayAxleCounter(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()