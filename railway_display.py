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
        self.root.title("Railway Axle Counter System - ADLD Project")
        
        # Make window larger to accommodate circuit viewer
        self.root.geometry("800x600")
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
        
        # Setup GUI with scrollbar
        self.setup_gui()
        
        # Connect to Arduinos
        self.connect_arduinos()
        
        # Start serial reader threads
        self.running = True
        self.start_serial_threads()
        
    def setup_gui(self):
        # Create main container with scrollbar
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Create scrollable frame
        self.scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # ============ SECTION 1: MAIN CONTROL PANEL ============
        self.create_control_panel()
        
        # ============ SECTION 2: CIRCUIT VISUALIZER ============
        self.create_circuit_visualizer()
        
    def create_control_panel(self):
        """Original control panel - top section"""
        control_container = tk.Frame(self.scrollable_frame, bg='#1a1a2e')
        control_container.pack(fill=tk.X, padx=10, pady=5)
        
        # Title Bar
        title_frame = tk.Frame(control_container, bg='#0f3460', height=40)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🚂 RAILWAY AXLE COUNTER - ADLD PROJECT",
            font=('Arial', 16, 'bold'),
            bg='#0f3460',
            fg='#ffffff'
        )
        title_label.pack(pady=5)
        
        # Main content area
        main_frame = tk.Frame(control_container, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
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
        
        # Reset button
        tk.Button(
            control_container,
            text="RESET COUNT",
            font=('Arial', 12, 'bold'),
            bg='#ff6b6b',
            fg='#ffffff',
            activebackground='#ff4444',
            command=self.reset_count,
            width=15,
            height=1
        ).pack(pady=10)
        
        # Status bar
        self.status_label = tk.Label(
            control_container,
            text="Initializing...",
            font=('Arial', 8),
            bg='#0f3460',
            fg='#aaaaaa',
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)
        
        # Separator
        tk.Frame(self.scrollable_frame, height=3, bg='#e94560').pack(fill=tk.X, pady=10)
    
    def create_circuit_visualizer(self):
        """Circuit diagram and 7-segment visualizer - scroll down to see"""
        
        # Section Title
        circuit_title = tk.Frame(self.scrollable_frame, bg='#0f3460')
        circuit_title.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            circuit_title,
            text="⚡ LIVE CIRCUIT VISUALIZER - BCD TO 7-SEGMENT",
            font=('Arial', 14, 'bold'),
            bg='#0f3460',
            fg='#ffffff'
        ).pack(pady=8)
        
        # Main circuit container
        circuit_frame = tk.Frame(self.scrollable_frame, bg='#16213e', relief=tk.RAISED, bd=3)
        circuit_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # ===== DECIMAL TO BINARY CONVERSION =====
        conversion_frame = tk.Frame(circuit_frame, bg='#1a2332', relief=tk.GROOVE, bd=2)
        conversion_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            conversion_frame,
            text="DECIMAL TO BINARY CONVERSION",
            font=('Arial', 12, 'bold'),
            bg='#1a2332',
            fg='#00ff88'
        ).pack(pady=5)
        
        # Tens digit
        tens_frame = tk.Frame(conversion_frame, bg='#1a2332')
        tens_frame.pack(pady=5)
        
        tk.Label(
            tens_frame,
            text="TENS DIGIT:",
            font=('Arial', 11, 'bold'),
            bg='#1a2332',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.tens_decimal_label = tk.Label(
            tens_frame,
            text="0",
            font=('Arial', 18, 'bold'),
            bg='#000000',
            fg='#00ff00',
            width=3,
            relief=tk.SUNKEN,
            bd=2
        )
        self.tens_decimal_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            tens_frame,
            text="→",
            font=('Arial', 16, 'bold'),
            bg='#1a2332',
            fg='#ffaa00'
        ).pack(side=tk.LEFT, padx=5)
        
        # Tens BCD bits
        self.tens_bcd_labels = []
        for i in range(4):
            label = tk.Label(
                tens_frame,
                text="0",
                font=('Arial', 16, 'bold'),
                bg='#000000',
                fg='#ff0000',
                width=2,
                relief=tk.RAISED,
                bd=3
            )
            label.pack(side=tk.LEFT, padx=2)
            self.tens_bcd_labels.append(label)
        
        tk.Label(
            tens_frame,
            text="D C B A",
            font=('Arial', 9),
            bg='#1a2332',
            fg='#888888'
        ).pack(side=tk.LEFT, padx=5)
        
        # Ones digit
        ones_frame = tk.Frame(conversion_frame, bg='#1a2332')
        ones_frame.pack(pady=5)
        
        tk.Label(
            ones_frame,
            text="ONES DIGIT:",
            font=('Arial', 11, 'bold'),
            bg='#1a2332',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.ones_decimal_label = tk.Label(
            ones_frame,
            text="0",
            font=('Arial', 18, 'bold'),
            bg='#000000',
            fg='#00ff00',
            width=3,
            relief=tk.SUNKEN,
            bd=2
        )
        self.ones_decimal_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            ones_frame,
            text="→",
            font=('Arial', 16, 'bold'),
            bg='#1a2332',
            fg='#ffaa00'
        ).pack(side=tk.LEFT, padx=5)
        
        # Ones BCD bits
        self.ones_bcd_labels = []
        for i in range(4):
            label = tk.Label(
                ones_frame,
                text="0",
                font=('Arial', 16, 'bold'),
                bg='#000000',
                fg='#ff0000',
                width=2,
                relief=tk.RAISED,
                bd=3
            )
            label.pack(side=tk.LEFT, padx=2)
            self.ones_bcd_labels.append(label)
        
        tk.Label(
            ones_frame,
            text="D C B A",
            font=('Arial', 9),
            bg='#1a2332',
            fg='#888888'
        ).pack(side=tk.LEFT, padx=5)
        
        # ===== CD4511 DECODER VISUALIZATION =====
        decoder_frame = tk.Frame(circuit_frame, bg='#1a2332', relief=tk.GROOVE, bd=2)
        decoder_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            decoder_frame,
            text="CD4511 BCD-TO-7-SEGMENT DECODER",
            font=('Arial', 12, 'bold'),
            bg='#1a2332',
            fg='#00ff88'
        ).pack(pady=5)
        
        tk.Label(
            decoder_frame,
            text="Arduino UNO Pins → BCD Input → CD4511 → 7-Segment Display",
            font=('Arial', 10),
            bg='#1a2332',
            fg='#aaaaaa'
        ).pack(pady=3)
        
        # ===== 7-SEGMENT DISPLAYS =====
        display_container = tk.Frame(circuit_frame, bg='#000000')
        display_container.pack(pady=20)
        
        tk.Label(
            display_container,
            text="LIVE 7-SEGMENT DISPLAY",
            font=('Arial', 12, 'bold'),
            bg='#000000',
            fg='#00ff88'
        ).pack(pady=10)
        
        # Display frame
        displays_frame = tk.Frame(display_container, bg='#000000')
        displays_frame.pack()
        
        # Tens display
        tens_display_frame = tk.Frame(displays_frame, bg='#000000')
        tens_display_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            tens_display_frame,
            text="TENS",
            font=('Arial', 10, 'bold'),
            bg='#000000',
            fg='#888888'
        ).pack()
        
        self.tens_canvas = tk.Canvas(tens_display_frame, width=100, height=150, bg='#000000', highlightthickness=0)
        self.tens_canvas.pack(pady=10)
        
        # Ones display
        ones_display_frame = tk.Frame(displays_frame, bg='#000000')
        ones_display_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            ones_display_frame,
            text="ONES",
            font=('Arial', 10, 'bold'),
            bg='#000000',
            fg='#888888'
        ).pack()
        
        self.ones_canvas = tk.Canvas(ones_display_frame, width=100, height=150, bg='#000000', highlightthickness=0)
        self.ones_canvas.pack(pady=10)
        
        # ===== PIN MAPPING TABLE =====
        pin_frame = tk.Frame(circuit_frame, bg='#1a2332', relief=tk.GROOVE, bd=2)
        pin_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            pin_frame,
            text="ARDUINO UNO PIN MAPPING",
            font=('Arial', 11, 'bold'),
            bg='#1a2332',
            fg='#00ff88'
        ).pack(pady=5)
        
        pin_info = tk.Frame(pin_frame, bg='#1a2332')
        pin_info.pack(pady=5)
        
        # Left column
        left_pins = tk.Frame(pin_info, bg='#1a2332')
        left_pins.pack(side=tk.LEFT, padx=20)
        
        tk.Label(left_pins, text="ONES DIGIT BCD:", font=('Arial', 9, 'bold'), bg='#1a2332', fg='#ffaa00').pack(anchor=tk.W)
        tk.Label(left_pins, text="Pin D2 → A (bit 0)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        tk.Label(left_pins, text="Pin D3 → B (bit 1)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        tk.Label(left_pins, text="Pin D4 → C (bit 2)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        tk.Label(left_pins, text="Pin D5 → D (bit 3)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        
        # Right column
        right_pins = tk.Frame(pin_info, bg='#1a2332')
        right_pins.pack(side=tk.LEFT, padx=20)
        
        tk.Label(right_pins, text="TENS DIGIT BCD:", font=('Arial', 9, 'bold'), bg='#1a2332', fg='#ffaa00').pack(anchor=tk.W)
        tk.Label(right_pins, text="Pin D10 → A (bit 0)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        tk.Label(right_pins, text="Pin D11 → B (bit 1)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        tk.Label(right_pins, text="Pin D12 → C (bit 2)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        tk.Label(right_pins, text="Pin D13 → D (bit 3)", font=('Arial', 9), bg='#1a2332', fg='#ffffff').pack(anchor=tk.W)
        
        # Project info
        info_frame = tk.Frame(self.scrollable_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            info_frame,
            text="ADLD (Advanced Digital Logic Design) Project",
            font=('Arial', 11, 'bold'),
            bg='#0f3460',
            fg='#ffffff'
        ).pack(pady=3)
        
        tk.Label(
            info_frame,
            text="Railway Axle Counter with BCD Display & Temperature Monitoring",
            font=('Arial', 9),
            bg='#0f3460',
            fg='#aaaaaa'
        ).pack(pady=2)
        
    def draw_seven_segment(self, canvas, digit, color='#ff0000'):
        """Draw a 7-segment display showing the given digit"""
        canvas.delete("all")
        
        # Segment positions (x1, y1, x2, y2)
        segments = {
            'a': [(20, 10, 80, 10), (25, 5, 75, 15)],   # top
            'b': [(80, 10, 80, 60), (75, 15, 85, 55)],  # top-right
            'c': [(80, 70, 80, 120), (75, 75, 85, 115)], # bottom-right
            'd': [(20, 120, 80, 120), (25, 115, 75, 125)], # bottom
            'e': [(20, 70, 20, 120), (15, 75, 25, 115)], # bottom-left
            'f': [(20, 10, 20, 60), (15, 15, 25, 55)],  # top-left
            'g': [(20, 65, 80, 65), (25, 60, 75, 70)]   # middle
        }
        
        # Segment patterns for each digit (which segments to light up)
        patterns = {
            0: ['a', 'b', 'c', 'd', 'e', 'f'],
            1: ['b', 'c'],
            2: ['a', 'b', 'd', 'e', 'g'],
            3: ['a', 'b', 'c', 'd', 'g'],
            4: ['b', 'c', 'f', 'g'],
            5: ['a', 'c', 'd', 'f', 'g'],
            6: ['a', 'c', 'd', 'e', 'f', 'g'],
            7: ['a', 'b', 'c'],
            8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            9: ['a', 'b', 'c', 'd', 'f', 'g']
        }
        
        # Draw all segments
        active_segments = patterns.get(digit, [])
        
        for seg_name, coords in segments.items():
            if seg_name in active_segments:
                # Active segment - bright red
                canvas.create_polygon(
                    coords[1],
                    fill=color,
                    outline=color,
                    width=2
                )
            else:
                # Inactive segment - dark gray
                canvas.create_polygon(
                    coords[1],
                    fill='#1a1a1a',
                    outline='#333333',
                    width=1
                )
    
    def update_circuit_visualizer(self):
        """Update the circuit visualizer with current count"""
        tens = (self.axle_count // 10) % 10
        ones = self.axle_count % 10
        
        # Update decimal labels
        self.tens_decimal_label.config(text=str(tens))
        self.ones_decimal_label.config(text=str(ones))
        
        # Update BCD binary representation
        for i in range(4):
            # Tens digit BCD
            bit_value = (tens >> i) & 1
            self.tens_bcd_labels[i].config(
                text=str(bit_value),
                fg='#00ff00' if bit_value else '#ff0000',
                bg='#003300' if bit_value else '#330000'
            )
            
            # Ones digit BCD
            bit_value = (ones >> i) & 1
            self.ones_bcd_labels[i].config(
                text=str(bit_value),
                fg='#00ff00' if bit_value else '#ff0000',
                bg='#003300' if bit_value else '#330000'
            )
        
        # Update 7-segment displays
        self.draw_seven_segment(self.tens_canvas, tens)
        self.draw_seven_segment(self.ones_canvas, ones)
    
    def connect_arduinos(self):
        UNO_PORT = '/dev/ttyACM0'
        NANO_PORT = '/dev/ttyUSB0'
        
        try:
            self.uno_serial = serial.Serial(UNO_PORT, 115200, timeout=1)
            time.sleep(2)
            self.update_status(f"✓ UNO connected on {UNO_PORT}")
            print(f"UNO connected: {UNO_PORT}")
        except Exception as e:
            self.update_status(f"✗ UNO connection failed: {e}")
            print(f"UNO error: {e}")
        
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
            self.update_circuit_visualizer()  # Update circuit view!
        elif msg.startswith("MATCH:"):
            self.match_status = (msg.split(":")[1] == "TRUE")
            self.update_match_display()
        elif msg == "UNO_READY":
            self.update_status("UNO Ready")
            self.update_circuit_visualizer()  # Initialize display
    
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
    
    def update_count_display(self):
        self.count_label.config(text=f"{self.axle_count:02d}")
        
        if self.compare_mode and self.target_count > 0:
            if self.axle_count == self.target_count:
                self.count_label.config(fg='#00ff00')
            elif self.axle_count > self.target_count:
                self.count_label.config(fg='#ff0000')
            else:
                self.count_label.config(fg='#ffaa00')
        else:
            self.count_label.config(fg='#00ff00')
    
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
            target = self.show_target_entry_dialog()
            
            if target is not None:
                self.compare_mode = True
                self.target_count = target
                self.target_label.config(text=f"{target:02d}")
                self.mode_button.config(text="COMPARE", bg='#e94560')
                self.send_to_uno("MODE:COMPARE\n")
                self.send_to_uno(f"TARGET:{target}\n")
                self.update_status(f"Compare mode - Target: {target}")
            else:
                self.update_status("Cancelled - staying in COUNT mode")
        else:
            self.compare_mode = False
            self.mode_button.config(text="COUNT", bg='#0f3460')
            self.send_to_uno("MODE:COUNT\n")
            self.match_label.config(text="")
            self.target_label.config(text="--")
            self.target_count = 0
            self.update_status("Count mode - no target")
    
    def show_target_entry_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Target Axle Count")
        dialog.geometry("350x200")
        dialog.configure(bg='#1a1a2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"350x200+{x}+{y}")
        
        result = [None]
        
        tk.Label(
            dialog,
            text="Enter Target Axle Count",
            font=('Arial', 16, 'bold'),
            bg='#1a1a2e',
            fg='#e94560'
        ).pack(pady=20)
        
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
        
        entry.bind('<Return>', lambda e: submit())
        
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
        
        dialog.wait_window()
        return result[0]
    
    def reset_count(self):
        self.send_to_uno("RESET\n")
        self.axle_count = 0
        self.update_count_display()
        self.update_circuit_visualizer()  # Update circuit view
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