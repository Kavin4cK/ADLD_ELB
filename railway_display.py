#!/usr/bin/env python3
import tkinter as tk
from tkinter import font as tkfont, simpledialog
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
        
        # Target Display (NO ENTRY BOX HERE)
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
            text="--",
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
        
        # Mode Toggle Button - LARGER
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
            font=('Arial', 14, 'bold'),
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#e94560',
            command=self.toggle_mode,
            width=10,
            height=2
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
        
        # Bottom Panel - Reset Button
        bottom_frame = tk.Frame(self.root, bg='#0f3460')
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            bottom_frame,
            text="RESET COUNT",
            font=('Arial', 12, 'bold'),
            bg='#ff6b6b',
            fg='#ffffff',
            activebackground='#ff4444',
            command=self.reset_count,
            width=15,
            height=1
        ).pack(pady=5)
        
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
        # CORRECT PORTS
        UNO_PORT = '/dev/ttyACM0'
        NANO_PORT = '/dev/ttyUSB0'
        
        # Connect to UNO
        try:
            self.uno_serial = serial.Serial(UNO_PORT, 115200, timeout=1)
            time.sleep(2)
            self.update_status(f"✓ UNO connected on {UNO_PORT}")
            print(f"UNO connected: {UNO_PORT}")
        except Exception as e:
            self.update_status(f"✗ UNO connection failed: {e}")
            print(f"UNO error: {e}")
        
        # Connect to Nano
        try:
            self.nano_serial = serial.Serial(NANO_PORT, 115200, timeout=1)
            time.sleep(2)
            self.update_status(f"✓ Nano connected on {NANO_PORT}")
            print(f"Nano connected: {NANO_PORT}")
        except Exception as e:
            self.update_status(f"✗ Nano connection failed: {e}")
            print(f"Nano error: {e}")
    
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
                    line = self.uno_serial.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"UNO → {line}")
                        self.process_uno_message(line)
            except Exception as e:
                print(f"UNO read error: {e}")
            time.sleep(0.01)
    
    def read_nano_serial(self):
        while self.running:
            try:
                if self.nano_serial and self.nano_serial.in_waiting:
                    line = self.nano_serial.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"NANO → {line}")
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
        elif msg.startswith("DEBUG:"):
            pass
    
    def process_nano_message(self, msg):
        if msg.startswith("TEMP:"):
            try:
                self.temperature = float(msg.split(":")[1])
                self.update_temp_display()
            except:
                pass
        elif msg == "HOT_AXLE_ALERT":
            self.hot_axle = True
            self.update_temp_display()
        elif msg == "NANO_READY":
            self.update_status("Nano Ready")
        elif msg.startswith("DEBUG:"):
            pass
    
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
        if self.temperature > -50:
            self.temp_label.config(text=f"{self.temperature:.1f}°C")
            
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
        if not self.compare_mode:
            # Switching TO compare mode - show popup to enter target
            target = self.show_target_entry_dialog()
            
            if target is not None:  # User entered a valid target
                self.compare_mode = True
                self.target_count = target
                self.target_label.config(text=f"{target:02d}")
                self.mode_button.config(text="COMPARE", bg='#e94560')
                self.send_to_uno("MODE:COMPARE\n")
                self.send_to_uno(f"TARGET:{target}\n")
                self.update_status(f"Compare mode - Target: {target}")
            else:
                # User cancelled - stay in count mode
                self.update_status("Cancelled - staying in COUNT mode")
        else:
            # Switching FROM compare mode to count mode
            self.compare_mode = False
            self.mode_button.config(text="COUNT", bg='#0f3460')
            self.send_to_uno("MODE:COUNT\n")
            self.match_label.config(text="")
            self.target_label.config(text="--")
            self.target_count = 0
            self.update_status("Count mode - no target")
    
    def show_target_entry_dialog(self):
        """Show a custom popup dialog to enter target number"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Target Axle Count")
        dialog.geometry("350x200")
        dialog.configure(bg='#1a1a2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"350x200+{x}+{y}")
        
        result = [None]  # Use list to store result from inner function
        
        # Title
        tk.Label(
            dialog,
            text="Enter Target Axle Count",
            font=('Arial', 16, 'bold'),
            bg='#1a1a2e',
            fg='#e94560'
        ).pack(pady=20)
        
        # Entry box
        entry_frame = tk.Frame(dialog, bg='#1a1a2e')
        entry_frame.pack(pady=10)
        
        entry = tk.Entry(
            entry_frame,
            font=('Arial', 24, 'bold'),
            width=5,
            bg='#ffffff',
            fg='#000000',
            justify='center',
            bd=3,
            relief=tk.SUNKEN
        )
        entry.pack()
        entry.focus_set()
        
        # Error label
        error_label = tk.Label(
            dialog,
            text="",
            font=('Arial', 10),
            bg='#1a1a2e',
            fg='#ff6b6b'
        )
        error_label.pack()
        
        def submit():
            try:
                value = int(entry.get())
                if 1 <= value <= 99:
                    result[0] = value
                    dialog.destroy()
                else:
                    error_label.config(text="Please enter 1-99")
            except ValueError:
                error_label.config(text="Invalid number")
        
        def cancel():
            result[0] = None
            dialog.destroy()
        
        # Bind Enter key
        entry.bind('<Return>', lambda e: submit())
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#1a1a2e')
        button_frame.pack(pady=15)
        
        tk.Button(
            button_frame,
            text="SET TARGET",
            font=('Arial', 12, 'bold'),
            bg='#e94560',
            fg='#ffffff',
            activebackground='#ff6b6b',
            command=submit,
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="CANCEL",
            font=('Arial', 12, 'bold'),
            bg='#0f3460',
            fg='#ffffff',
            activebackground='#1a3a5a',
            command=cancel,
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result[0]
    
    def reset_count(self):
        self.send_to_uno("RESET\n")
        self.axle_count = 0
        self.update_count_display()
        self.match_label.config(text="")
        self.update_status("✓ Count reset to 0")
    
    def send_to_uno(self, message):
        try:
            if self.uno_serial:
                with self.serial_lock:
                    self.uno_serial.write(message.encode())
                    print(f"SENT TO UNO: {message.strip()}")
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