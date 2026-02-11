#!/usr/bin/env python3
import serial
import time

print("=== Arduino Serial Port Finder ===\n")

# Try common ports
ports_to_try = [
    '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2',
    '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2'
]

for port in ports_to_try:
    try:
        print(f"Trying {port}...", end=" ")
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(2)  # Wait for Arduino to reset
        
        # Read for 3 seconds
        print("LISTENING...")
        start = time.time()
        while time.time() - start < 3:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"  → {line}")
        
        ser.close()
        print(f"✓ {port} is active\n")
        
    except serial.SerialException:
        print("Not found")
    except Exception as e:
        print(f"Error: {e}")

print("\n=== Done ===")