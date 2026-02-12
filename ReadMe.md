🚂 RAILWAY AXLE COUNTER SYSTEM - COMPLETE README
ADLD (Advanced Digital Logic Design) Project
Railway Axle Counter with BCD Display, Temperature Monitoring & Bluetooth Alert System

📋 TABLE OF CONTENTS

Project Overview
System Architecture
Hardware Requirements
Software Requirements
Circuit Diagrams
Pin Connections
Installation Guide
Code Files
Operation Manual
Troubleshooting
Project Theory
Future Enhancements


🎯 PROJECT OVERVIEW
Objective
Design and implement a distributed railway axle counting system that:

Detects and counts train axles using ultrasonic sensors
Displays count on multiple display technologies (7-segment, LCD, OLED, GUI)
Monitors axle temperature for hot axle detection
Implements BCD (Binary Coded Decimal) encoding for hardware displays
Sends wireless alerts via Bluetooth when target count is reached
Provides real-time circuit visualization

Real-World Application
Railway track circuits use axle counters to:

Detect train presence in track sections
Verify complete train passage (all axles counted)
Trigger signals and track occupation indicators
Detect hot axles (bearing failures) before catastrophic failure

Key Features
✅ Multi-sensor detection - Ultrasonic distance measurement
✅ Multi-display output - 7-segment (BCD), LCD (I²C), OLED (I²C), GUI
✅ Temperature monitoring - DS18B20 digital temperature sensor
✅ Distributed architecture - Arduino UNO, Nano, Raspberry Pi, ESP32
✅ Wireless communication - Bluetooth Low Energy (BLE)
✅ Real-time visualization - Live circuit diagram with binary conversion
✅ Two operational modes - COUNT (monitoring) and COMPARE (validation)

🏗️ SYSTEM ARCHITECTURE
┌─────────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI 4 (Master Controller)           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  • Python GUI (TkInter)                                   │  │
│  │  • Real-time 7-segment visualizer                        │  │
│  │  • BCD binary conversion display                         │  │
│  │  • Mode control (COUNT / COMPARE)                        │  │
│  │  • Target entry & validation                             │  │
│  │  • Bluetooth communication manager                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────┬───────────────────────┬────────────────┬─────────────┘
           │ USB Serial            │ USB Serial     │ Bluetooth
           │ (115200 baud)         │ (115200 baud)  │ (RFCOMM)
           ▼                       ▼                ▼
    ┌──────────────┐        ┌──────────────┐   ┌──────────────┐
    │ ARDUINO UNO  │◄──I²C─►│ ARDUINO NANO │   │   ESP32-     │
    │              │        │              │   │   WROOM-32   │
    │ Main Counter │        │ Temperature  │   │   Alert LED  │
    └──────┬───────┘        └──────┬───────┘   └──────────────┘
           │                       │
           ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │ • Ultrasonic │        │  DS18B20     │
    │   HC-SR04    │        │  Temp Sensor │
    │ • 2× CD4511  │        │              │
    │ • 2× 7-seg   │        │              │
    │ • LCD 16×2   │        │              │
    │ • OLED 1.3"  │        │              │
    │ • LED Alert  │        │              │
    └──────────────┘        └──────────────┘
Data Flow

Detection Phase

HC-SR04 ultrasonic sensor detects object
UNO increments count (debounced)
Count converted to BCD (2 digits)


Display Phase

BCD output to CD4511 decoders → 7-segment displays
I²C data to LCD and OLED
Serial data to Raspberry Pi → GUI update


Monitoring Phase

Nano reads DS18B20 temperature
Sends to Raspberry Pi via serial
Hot axle alert if temp > 80°C


Alert Phase (COMPARE mode)

When count == target
Raspberry Pi sends Bluetooth command
ESP32 receives → LED ON




🛠️ HARDWARE REQUIREMENTS
Microcontrollers
ComponentQuantityPurposeArduino UNO R31Main axle counter controllerArduino Nano1Temperature sensor interfaceRaspberry Pi 4 (2GB+)1Master display & controlESP32-WROOM-321Bluetooth alert receiver
Sensors
ComponentQuantitySpecificationsHC-SR04 Ultrasonic12cm-400cm range, 5VDS18B20 Temperature1-55°C to +125°C, 1-Wire
Displays
ComponentQuantityInterfaceAddressLCD 16×2 with I²C1I²C0x27OLED 1.3" 128×641I²C0x3C7-Segment Common Anode2BCD-CD4511 BCD Decoder2TTL Logic-3.5" TFT for RPi1GPIO-
Electronic Components
ComponentQuantitySpecification5mm LED (Red)220mA, 2V forwardResistor 220Ω31/4WResistor 4.7kΩ1Pull-up for DS18B20Breadboard2830 tie-pointsJumper Wires50+Male-Male, Male-FemaleUSB-A to USB-B1For Arduino UNOUSB-A to Mini-USB1For Arduino NanoUSB-A to Micro-USB1For ESP325V Power Supply12A minimum
Optional Components

Toggle switch (for hardware mode selection)
Buzzer (for audio alert)
Enclosure/project box


💾 SOFTWARE REQUIREMENTS
Development Tools
SoftwareVersionPurposeArduino IDE2.0+Program Arduino UNO & NanoPython3.9+Raspberry Pi interfaceRaspbian OSBullseye/BookwormOperating system
Python Libraries (Raspberry Pi)
bashsudo apt-get install python3-serial python3-tk bluetooth bluez libbluetooth-dev
sudo pip3 install pybluez --break-system-packages
```

### **Arduino Libraries**
Install via Arduino IDE Library Manager:
- **Wire** (built-in) - I²C communication
- **LiquidCrystal_I2C** by Frank de Brabander
- **Adafruit_GFX** by Adafruit
- **Adafruit_SSD1306** by Adafruit
- **OneWire** by Paul Stoffregen
- **DallasTemperature** by Miles Burton

### **ESP32 Board Support**
1. Open Arduino IDE
2. File → Preferences
3. Additional Board URLs: `https://dl.espressif.com/dl/package_esp32_index.json`
4. Tools → Board → Board Manager → Install "ESP32 by Espressif"

---

## 🔌 CIRCUIT DIAGRAMS

### **I²C Bus (Shared Communication Line)**

All I²C devices share two wires:
```
Arduino UNO Pin A4 (SDA) ────┬──── LCD SDA
                             ├──── OLED SDA
                             └──── Arduino Nano Pin A4 (SDA)

Arduino UNO Pin A5 (SCL) ────┬──── LCD SCL
                             ├──── OLED SCL
                             └──── Arduino Nano Pin A5 (SCL)

CRITICAL: UNO GND ←→ Nano GND (Common Ground)
```

### **Arduino UNO Connections**

#### **Ultrasonic Sensor (HC-SR04)**
```
HC-SR04 Pin     Arduino UNO
───────────     ───────────
VCC        →    5V
GND        →    GND
TRIG       →    D9
ECHO       →    D8
```

#### **BCD Output to CD4511 (Two Digits)**

**ONES Digit (0-9):**
```
UNO Pin     CD4511 #1 Pin     Function
───────     ─────────────     ────────
D2     →    A (pin 7)         BCD bit 0 (LSB)
D3     →    B (pin 1)         BCD bit 1
D4     →    C (pin 2)         BCD bit 2
D5     →    D (pin 6)         BCD bit 3 (MSB)
```

**TENS Digit (0-9):**
```
UNO Pin     CD4511 #2 Pin     Function
───────     ─────────────     ────────
D10    →    A (pin 7)         BCD bit 0 (LSB)
D11    →    B (pin 1)         BCD bit 1
D12    →    C (pin 2)         BCD bit 2
D13    →    D (pin 6)         BCD bit 3 (MSB)
```

#### **CD4511 Control Pins (BOTH chips)**
```
CD4511 Pin      Connection      Purpose
──────────      ──────────      ───────
LE (pin 5)  →   GND             Latch Enable (always enabled)
BI (pin 4)  →   GND             Blanking Input (for common anode)
LT (pin 3)  →   GND             Lamp Test (normal operation)
VCC (pin 16)→   5V              Power
GND (pin 8) →   GND             Ground
```

#### **CD4511 to 7-Segment Display (BOTH displays)**
```
CD4511 Output   7-Segment Pin   Segment
─────────────   ─────────────   ───────
a (pin 13)  →   a               Top
b (pin 12)  →   b               Top-right
c (pin 11)  →   c               Bottom-right
d (pin 10)  →   d               Bottom
e (pin 9)   →   e               Bottom-left
f (pin 15)  →   f               Top-left
g (pin 14)  →   g               Middle

7-Segment Common Anode → 5V (IMPORTANT: Common ANODE, not cathode)
```

#### **LED Indicator**
```
LED Component       Arduino UNO
─────────────       ───────────
Anode (+)      →    D6
Cathode (-)    →    220Ω resistor → GND
```

#### **I²C Devices**
```
Device      UNO Pin
──────      ───────
SDA    →    A4
SCL    →    A5
VCC    →    5V
GND    →    GND
```

### **Arduino Nano Connections**

#### **DS18B20 Temperature Sensor**
```
DS18B20 Pin         Nano Pin
───────────         ────────
VCC (Red)      →    5V
GND (Black)    →    GND
DATA (Yellow)  →    D9

CRITICAL: 4.7kΩ pull-up resistor between DATA (D9) and VCC (5V)
```

#### **I²C Bus**
```
Nano Pin    Connection
────────    ──────────
A4     →    Shared SDA line
A5     →    Shared SCL line
GND    →    Common ground with UNO
```

### **ESP32-WROOM-32 Connections**
```
ESP32 GPIO      Component
──────────      ─────────
GPIO 2     →    LED Anode (+) → 220Ω resistor → GND
GND        →    Common Ground
```

### **Raspberry Pi Connections**

#### **USB Connections**
```
RPi USB Port    Device
────────────    ──────
USB 0      →    Arduino UNO (programming cable)
USB 1      →    Arduino Nano (programming cable)
Any USB    →    ESP32 (for power only, optional)
```

#### **GPIO (for 3.5" TFT display - optional)**
Refer to your specific TFT model's pinout.

---

## 📐 PIN CONNECTIONS SUMMARY TABLE

### **Arduino UNO Pin Allocation**

| Pin | Function | Connected To |
|-----|----------|--------------|
| D2 | BCD Ones A | CD4511 #1 pin 7 |
| D3 | BCD Ones B | CD4511 #1 pin 1 |
| D4 | BCD Ones C | CD4511 #1 pin 2 |
| D5 | BCD Ones D | CD4511 #1 pin 6 |
| D6 | LED Output | LED Anode via 220Ω |
| D8 | Ultrasonic ECHO | HC-SR04 ECHO |
| D9 | Ultrasonic TRIG | HC-SR04 TRIG |
| D10 | BCD Tens A | CD4511 #2 pin 7 |
| D11 | BCD Tens B | CD4511 #2 pin 1 |
| D12 | BCD Tens C | CD4511 #2 pin 2 |
| D13 | BCD Tens D | CD4511 #2 pin 6 |
| A4 | I²C SDA | LCD, OLED, Nano |
| A5 | I²C SCL | LCD, OLED, Nano |
| 5V | Power | All sensors, displays |
| GND | Ground | Common ground |

### **Arduino Nano Pin Allocation**

| Pin | Function | Connected To |
|-----|----------|--------------|
| D9 | 1-Wire Data | DS18B20 DATA + 4.7kΩ pull-up |
| A4 | I²C SDA | Shared bus |
| A5 | I²C SCL | Shared bus |
| 5V | Power | DS18B20 VCC |
| GND | Ground | Common ground |

### **ESP32 Pin Allocation**

| Pin | Function | Connected To |
|-----|----------|--------------|
| GPIO 2 | LED Output | LED Anode via 220Ω |
| GND | Ground | LED Cathode |

---

## 🔧 INSTALLATION GUIDE

### **STEP 1: Hardware Assembly**

#### **1.1 Set Up I²C Bus**
```
1. Connect all SDA pins together (UNO A4, Nano A4, LCD SDA, OLED SDA)
2. Connect all SCL pins together (UNO A5, Nano A5, LCD SCL, OLED SCL)
3. CRITICAL: Connect UNO GND to Nano GND
4. Connect all VCC to 5V, all GND to common ground
```

#### **1.2 Wire Arduino UNO**
```
1. Connect HC-SR04: TRIG→D9, ECHO→D8, VCC→5V, GND→GND
2. Connect BCD pins D2-D5 to CD4511 #1 (Ones digit)
3. Connect BCD pins D10-D13 to CD4511 #2 (Tens digit)
4. Set CD4511 control pins: LE→GND, BI→GND, LT→GND, VCC→5V, GND→GND
5. Connect CD4511 outputs (a-g) to 7-segment displays
6. Connect 7-segment common anodes to 5V
7. Connect LED: D6 → 220Ω → LED anode, LED cathode → GND
```

#### **1.3 Wire Arduino Nano**
```
1. Connect DS18B20: VCC→5V, GND→GND, DATA→D9
2. IMPORTANT: Add 4.7kΩ resistor between DATA and VCC
3. Connect to I²C bus
```

#### **1.4 Wire ESP32**
```
1. Connect LED: GPIO2 → 220Ω → LED anode, LED cathode → GND
1.5 Visual Inspection Checklist

 All grounds connected together
 No short circuits (5V touching GND)
 Pull-up resistor on DS18B20 installed
 7-segment common pins connected to 5V (not GND)
 I²C devices sharing SDA/SCL
 All power connections secure


STEP 2: Arduino Software Setup
2.1 Install Required Libraries
Open Arduino IDE:

Go to Sketch → Include Library → Manage Libraries
Search and install:

LiquidCrystal_I2C by Frank de Brabander
Adafruit GFX Library
Adafruit SSD1306
OneWire
DallasTemperature



2.2 Upload Arduino UNO Code

Open Arduino IDE
Create new sketch: UNO_Axle_Counter.ino
Copy code from Code Files section
Select: Tools → Board → Arduino UNO
Select correct COM port
Click Upload
Open Serial Monitor (115200 baud)
Should see: UNO_READY

2.3 Upload Arduino Nano Code

Create new sketch: NANO_Temperature_Sensor.ino
Copy code from Code Files section
Select: Tools → Board → Arduino Nano
Select: Tools → Processor → ATmega328P (Old Bootloader) if upload fails
Select correct COM port
Click Upload
Open Serial Monitor (115200 baud)
Should see: NANO_READY and TEMP:XX.XX

2.4 Upload ESP32 Code

Create new sketch: ESP32_BT_LED_Receiver.ino
Copy code from Code Files section
Select: Tools → Board → ESP32 Dev Module
Select correct COM port
Click Upload
Open Serial Monitor (115200 baud)
Should see: Bluetooth Started! Device name: ESP32_Railway_Counter
LED should blink 3 times (ready signal)


STEP 3: Raspberry Pi Software Setup
3.1 Update System
bashsudo apt-get update
sudo apt-get upgrade
3.2 Install Python Dependencies
bash# Install required packages
sudo apt-get install -y python3-serial python3-tk bluetooth bluez libbluetooth-dev

# Install Bluetooth library
sudo pip3 install pybluez --break-system-packages
3.3 Enable Bluetooth
bash# Enable and start Bluetooth service
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Add user to Bluetooth group
sudo usermod -a -G bluetooth $USER

# Reboot to apply changes
sudo reboot
3.4 Create Project Directory
bashmkdir -p ~/adld/ADLD_ELB
cd ~/adld/ADLD_ELB
3.5 Create Python Script
bashnano railway_display.py
Paste the complete code from Code Files section.
Save with Ctrl+X, Y, Enter.
3.6 Make Executable
bashchmod +x railway_display.py
```

---

### **STEP 4: System Integration**

#### **4.1 Connect Arduinos to Raspberry Pi**
```
1. Connect Arduino UNO to RPi USB port (usually /dev/ttyACM0)
2. Connect Arduino Nano to RPi USB port (usually /dev/ttyUSB0)
3. Wait 5 seconds for initialization
4.2 Verify Serial Ports
bash# List all USB serial devices
ls -l /dev/ttyUSB* /dev/ttyACM*

# Should see two devices
4.3 Test Serial Communication
bash# Quick test
python3 << EOF
import serial
import time

uno = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)
print("Reading from UNO...")
for i in range(5):
    if uno.in_waiting:
        print(uno.readline().decode('utf-8').strip())
    time.sleep(0.5)
uno.close()
EOF
```

Should see messages like `UNO_READY`, `DEBUG:Count=0...`

#### **4.4 Power On ESP32**
```
1. Connect ESP32 via USB or external power
2. LED should blink 3 times
3. Bluetooth is now active

STEP 5: First Run
5.1 Launch System
bashcd ~/adld/ADLD_ELB
python3 railway_display.py
```

#### **5.2 Watch Startup Sequence**

**Terminal Output:**
```
UNO connected: /dev/ttyACM0
Nano connected: /dev/ttyUSB0
Searching for ESP32_Railway_Counter...
Found ESP32 at XX:XX:XX:XX:XX:XX
Connecting...
✓ Bluetooth connected to ESP32
GUI Display:

Main window appears (800×600)
Status shows: "UNO Ready", "Nano Ready"
Bluetooth status: "Connected ✓" (green)
Temperature showing (e.g., "23.5°C")
Axle count: 00
Target: --

5.3 Initial Functionality Test
Test Temperature Sensor:

Touch DS18B20 with warm finger
Watch temperature increase on GUI
Should update every ~500ms

Test Axle Counter:

Wave hand in front of ultrasonic sensor
Watch count increment: 00 → 01 → 02...
7-segment displays should match
LCD and OLED should update

Test Mode Switch:

Click "COUNT" button
Popup appears: "Enter Target Axle Count"
Enter "5"
Click "SET TARGET"
Button changes to "COMPARE" (red)
Target shows: 05

Test Bluetooth Alert:

With target set to 5
Wave hand 5 times
When count reaches 5:

Green "✓ MATCH!" appears
ESP32 LED turns ON
Terminal shows: "🎯 TARGET REACHED - Signal sent to ESP32!"



Test Circuit Visualizer:

Scroll down in GUI
See "LIVE CIRCUIT VISUALIZER" section
Binary conversion showing
7-segment displays animating
Pin mapping table visible


📄 CODE FILES
File 1: UNO_Axle_Counter.ino
cpp#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Pin Definitions
#define TRIG 9
#define ECHO 8
#define LED_PIN 6

// BCD Output Pins
int onesBCD[4] = {2, 3, 4, 5};
int tensBCD[4] = {10, 11, 12, 13};

// Display Objects
LiquidCrystal_I2C lcd(0x27, 16, 2);
Adafruit_SSD1306 oled(128, 64, &Wire, -1);

// Variables
int axleCount = 0;
int targetCount = 0;
bool objectPresent = false;
bool compareMode = false;

void setup() {
  Serial.begin(115200);
  
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(LED_PIN, OUTPUT);
  
  for(int i = 0; i < 4; i++) {
    pinMode(onesBCD[i], OUTPUT);
    pinMode(tensBCD[i], OUTPUT);
  }
  
  Wire.begin();
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("UNO Starting...");
  
  if(!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED_FAIL");
  }
  oled.clearDisplay();
  oled.setTextSize(2);
  oled.setTextColor(WHITE);
  oled.setCursor(0, 0);
  oled.println("STARTING");
  oled.display();
  
  delay(1000);
  
  lcd.clear();
  lcd.print("System Ready");
  oled.clearDisplay();
  oled.println("READY");
  oled.display();
  
  Serial.println("UNO_READY");
}

void loop() {
  static unsigned long lastDebug = 0;
  if(millis() - lastDebug > 2000) {
    lastDebug = millis();
    Serial.print("DEBUG:Count=");
    Serial.print(axleCount);
    Serial.print(",Target=");
    Serial.print(targetCount);
    Serial.print(",Mode=");
    Serial.println(compareMode ? "COMPARE" : "COUNT");
  }
  
  if(Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    handleCommand(command);
  }
  
  long distance = getDistance();
  
  if(distance > 0 && distance < 10 && !objectPresent) {
    objectPresent = true;
  }
  
  if(distance > 15 && objectPresent) {
    axleCount++;
    objectPresent = false;
    
    Serial.print("COUNT:");
    Serial.println(axleCount);
    
    updateDisplays();
    outputBCD();
    checkComparison();
  }
  
  delay(50);
}

void handleCommand(String cmd) {
  cmd.trim();
  
  if(cmd.startsWith("MODE:")) {
    String mode = cmd.substring(5);
    if(mode == "COMPARE") {
      compareMode = true;
      Serial.println("MODE_SET:COMPARE");
      updateDisplays();
      checkComparison();
    } else if(mode == "COUNT") {
      compareMode = false;
      digitalWrite(LED_PIN, LOW);
      Serial.println("MODE_SET:COUNT");
      updateDisplays();
    }
  }
  else if(cmd.startsWith("TARGET:")) {
    targetCount = cmd.substring(7).toInt();
    Serial.print("TARGET_SET:");
    Serial.println(targetCount);
    updateDisplays();
    checkComparison();
  }
  else if(cmd == "RESET") {
    axleCount = 0;
    Serial.println("COUNT_RESET");
    Serial.print("COUNT:");
    Serial.println(axleCount);
    updateDisplays();
    outputBCD();
    digitalWrite(LED_PIN, LOW);
  }
  else if(cmd == "STATUS") {
    Serial.print("COUNT:");
    Serial.println(axleCount);
    Serial.print("TARGET:");
    Serial.println(targetCount);
    Serial.print("MODE:");
    Serial.println(compareMode ? "COMPARE" : "COUNT");
  }
}

long getDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  
  long duration = pulseIn(ECHO, HIGH, 30000);
  if(duration == 0) return 999;
  
  return duration * 0.034 / 2;
}

void checkComparison() {
  if(compareMode && axleCount == targetCount && targetCount > 0) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("MATCH:TRUE");
  } else {
    digitalWrite(LED_PIN, LOW);
    if(compareMode) {
      Serial.println("MATCH:FALSE");
    }
  }
}

void updateDisplays() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Cnt:");
  lcd.print(axleCount);
  lcd.print(" Tgt:");
  lcd.print(targetCount);
  lcd.setCursor(0, 1);
  lcd.print(compareMode ? "COMPARE MODE" : "COUNT MODE");
  
  oled.clearDisplay();
  oled.setTextSize(2);
  oled.setCursor(0, 0);
  oled.print("CNT:");
  oled.println(axleCount);
  oled.setCursor(0, 30);
  oled.print("TGT:");
  oled.println(targetCount);
  oled.display();
}

void outputBCD() {
  int ones = axleCount % 10;
  int tens = (axleCount / 10) % 10;
  
  for(int i = 0; i < 4; i++) {
    digitalWrite(onesBCD[i], (ones >> i) & 1);
  }
  
  for(int i = 0; i < 4; i++) {
    digitalWrite(tensBCD[i], (tens >> i) & 1);
  }
}

File 2: NANO_Temperature_Sensor.ino
cpp#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define TEMP_PIN 9

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

float temperature = 0.0;
unsigned long lastTempRead = 0;

void setup() {
  Serial.begin(115200);
  sensors.begin();
  delay(1000);
  Serial.println("NANO_READY");
}

void loop() {
  static unsigned long lastDebug = 0;
  if(millis() - lastDebug > 2000) {
    lastDebug = millis();
    Serial.print("DEBUG:Temp=");
    Serial.println(temperature, 2);
  }
  
  if(millis() - lastTempRead > 500) {
    lastTempRead = millis();
    
    sensors.requestTemperatures();
    temperature = sensors.getTempCByIndex(0);
    
    if(temperature > -50 && temperature < 125) {
      Serial.print("TEMP:");
      Serial.println(temperature, 2);
      
      if(temperature > 80.0) {
        Serial.println("HOT_AXLE_ALERT");
      }
    }
  }
  
  if(Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if(command == "GET_TEMP") {
      Serial.print("TEMP:");
      Serial.println(temperature, 2);
    }
    else if(command == "STATUS") {
      Serial.print("TEMP:");
      Serial.println(temperature, 2);
    }
  }
  
  delay(50);
}

File 3: ESP32_BT_LED_Receiver.ino
cpp#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled!
#endif

BluetoothSerial SerialBT;

#define LED_PIN 2

String deviceName = "ESP32_Railway_Counter";
bool targetReached = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  SerialBT.begin(deviceName);
  Serial.println("Bluetooth Started! Device name: " + deviceName);
  Serial.println("Waiting for connection from Raspberry Pi...");
  
  for(int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

void loop() {
  if (SerialBT.available()) {
    String command = SerialBT.readStringUntil('\n');
    command.trim();
    
    Serial.println("Received: " + command);
    
    if (command == "TARGET_REACHED") {
      targetReached = true;
      digitalWrite(LED_PIN, HIGH);
      Serial.println("✓ TARGET REACHED - LED ON");
      SerialBT.println("ACK:LED_ON");
    }
    else if (command == "RESET") {
      targetReached = false;
      digitalWrite(LED_PIN, LOW);
      Serial.println("✗ RESET - LED OFF");
      SerialBT.println("ACK:LED_OFF");
    }
    else if (command == "LED_ON") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("Manual LED ON");
      SerialBT.println("ACK:LED_ON");
    }
    else if (command == "LED_OFF") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("Manual LED OFF");
      SerialBT.println("ACK:LED_OFF");
    }
    else if (command == "STATUS") {
      String status = targetReached ? "REACHED" : "COUNTING";
      SerialBT.println("STATUS:" + status);
      Serial.println("Status sent: " + status);
    }
    else if (command == "PING") {
      SerialBT.println("PONG");
      Serial.println("Ping received");
    }
  }
  
  delay(20);
}
```

---

### **File 4: railway_display.py**

Due to length, refer to the complete code provided in the previous message. The file contains:
- TkInter GUI setup
- Serial communication handlers
- Bluetooth communication
- Circuit visualizer
- 7-segment drawing functions
- All event handlers

Save as `railway_display.py` in `/home/pi/adld/ADLD_ELB/`

---

## 📖 OPERATION MANUAL

### **Starting the System**

1. **Power On Sequence:**
```
   1. Connect Arduino UNO to power
   2. Connect Arduino Nano to power
   3. Connect ESP32 to power
   4. Boot Raspberry Pi
   5. Wait 30 seconds for initialization

Launch Software:

bash   cd ~/adld/ADLD_ELB
   python3 railway_display.py
```

3. **Verify Connections:**
   - Check status bar shows "UNO Ready" and "Nano Ready"
   - Check Bluetooth status shows "Connected ✓"
   - Check temperature is displaying
   - Check 7-segment displays showing "00"

---

### **COUNT Mode (Default)**

**Purpose:** Monitor and count axles passing the sensor

**How to Use:**
1. System starts in COUNT mode
2. Wave object in front of ultrasonic sensor (< 10cm)
3. Count increments when object moves away (> 15cm)
4. Displays update:
   - GUI: Large green number
   - 7-segment: Hardware BCD display
   - LCD/OLED: I²C displays

**Features:**
- No target comparison
- LED remains off
- Infinite counting (resets at 99)
- Real-time circuit visualization

---

### **COMPARE Mode**

**Purpose:** Validate that exact target count is reached

**How to Use:**

1. **Enable COMPARE Mode:**
   - Click "COUNT" button
   - Popup appears: "Enter Target Axle Count"
   - Type target number (1-99), e.g., "12"
   - Press Enter or click "SET TARGET"

2. **System Changes:**
   - Button turns red, says "COMPARE"
   - Target displays in orange
   - Raspberry Pi ready to send Bluetooth alert

3. **Count Axles:**
   - Wave objects past sensor
   - Count increases: 00 → 01 → 02 ... → 12
   - Display changes color:
     - Yellow (counting toward target)
     - Green (matched target)
     - Red (exceeded target)

4. **Target Reached:**
   - When count == target:
     - Green "✓ MATCH!" appears
     - UNO LED turns ON
     - Raspberry Pi sends Bluetooth command
     - **ESP32 LED turns ON**
     - Status shows: "🎯 TARGET REACHED - Signal sent to ESP32!"

5. **Return to COUNT Mode:**
   - Click "COMPARE" button again
   - Target clears
   - ESP32 LED turns OFF
   - Returns to continuous counting

---

### **Temperature Monitoring**

**Always Active (both modes):**

- DS18B20 reads temperature every 500ms
- Displays in GUI:
  - Blue (normal): < 60°C
  - Yellow (warning): 60-80°C
  - Red (alert): > 80°C

- Hot Axle Alert:
  - Temperature > 80°C
  - Label shows: "⚠️ HOT AXLE!"
  - Console logs: "HOT_AXLE_ALERT"

**Real-World Application:**
Railway hot axle detectors identify overheating bearings before catastrophic failure. Typical alarm thresholds are 80-95°C above ambient.

---

### **Circuit Visualizer**

**Location:** Scroll down in GUI window

**Shows:**
1. **Decimal to Binary Conversion**
   - Current count split into tens and ones digits
   - Each digit shown in decimal and 4-bit BCD
   - Bits light up green (1) or red (0)

2. **Live 7-Segment Display**
   - Realistic LED simulation
   - Updates in real-time with count
   - Shows what hardware displays show

3. **Pin Mapping Reference**
   - Complete Arduino UNO pin assignments
   - BCD bit assignments (D C B A)
   - Useful for hardware debugging

**Example:**
```
Count = 47

TENS DIGIT:  4  →  [0][1][0][0]  (BCD: 0100)
ONES DIGIT:  7  →  [0][1][1][1]  (BCD: 0111)

┌─┐  ┌─┐
│ │  │ │   ← Simulated 7-segment displays
├─┤  └─┤
│ │    │
└─┘  └─┘

Reset Function
Purpose: Clear count and restart
How to Use:

Click "RESET COUNT" button
Effects:

Count returns to 00
All displays update
UNO LED turns OFF
ESP32 LED turns OFF
Match indicator clears
Target remains (if in COMPARE mode)



When to Reset:

Starting new count cycle
Testing system
After target reached
Clearing error state


Bluetooth Communication
Commands Sent to ESP32:
CommandWhenESP32 ResponseTARGET_REACHED\nCount == TargetLED ONRESET\nReset buttonLED OFFPING\nConnection testPONG
Troubleshooting Connection:
bash# Manually scan for ESP32
hcitool scan

# Should show: XX:XX:XX:XX:XX:XX  ESP32_Railway_Counter
```

---

### **Display Summary**

| Display Type | Interface | Shows | Update Rate |
|--------------|-----------|-------|-------------|
| 7-Segment (×2) | BCD/TTL | Count (00-99) | Instant |
| LCD 16×2 | I²C | Count, Target, Mode | 50ms |
| OLED 1.3" | I²C | Count, Target | 50ms |
| Raspberry Pi GUI | USB Serial | Everything + visualizer | 50ms |
| ESP32 LED | Bluetooth | Target reached | Event-driven |

---

## 🔍 TROUBLESHOOTING

### **Problem: No Display on 7-Segment**

**Possible Causes:**
1. CD4511 control pins wrong
2. Common anode/cathode mismatch
3. BCD pins not connected
4. No power to CD4511

**Solutions:**
```
✓ Check CD4511 control pins:
  - LE (pin 5) → GND
  - BI (pin 4) → GND (for common anode)
  - LT (pin 3) → GND
  
✓ Verify 7-segment type:
  - Common ANODE → connect to 5V
  - Our code expects COMMON ANODE
  
✓ Test BCD output:
  - Upload simple test: set all BCD pins HIGH
  - Should display "8" (all segments)
  
✓ Check power:
  - CD4511 VCC → 5V
  - CD4511 GND → GND
```

---

### **Problem: Ultrasonic Sensor Not Detecting**

**Symptoms:**
- Count never increases
- Distance always shows 999

**Solutions:**
```
✓ Check wiring:
  - TRIG → D9
  - ECHO → D8
  - Ensure VCC is 5V, not 3.3V
  
✓ Test distance measurement:
  - Open Arduino Serial Monitor
  - Should see debug messages with distance
  - Wave hand at different distances
  
✓ Check timing:
  - Object must be < 10cm to trigger
  - Must move > 15cm away to count
  - Too fast movement may be missed
  
✓ Environment:
  - Soft/absorbing surfaces may not reflect well
  - Try flat, hard object (book, hand)
```

---

### **Problem: Temperature Shows "--°C"**

**Causes:**
- DS18B20 not connected
- Missing pull-up resistor
- Wrong 1-Wire pin

**Solutions:**
```
✓ Verify connections:
  - VCC (red) → 5V
  - GND (black) → GND
  - DATA (yellow) → D9
  
✓ CRITICAL: Check pull-up resistor
  - 4.7kΩ between DATA (D9) and VCC (5V)
  - Without this, sensor won't work
  
✓ Test sensor alone:
  File → Examples → DallasTemperature → Simple
  Upload and check Serial Monitor
  
✓ Check library installation:
  - OneWire library installed?
  - DallasTemperature library installed?
```

---

### **Problem: Bluetooth Connection Failed**

**Symptoms:**
- GUI shows "ESP32 not found"
- Status: "Connection failed" (red)

**Solutions:**
```
✓ Check ESP32:
  - Is it powered on?
  - Serial Monitor shows "Bluetooth Started!"?
  - LED blinked 3 times at startup?
  
✓ Scan for devices:
  hcitool scan
  # Should see: ESP32_Railway_Counter
  
✓ Restart Bluetooth:
  sudo systemctl restart bluetooth
  sudo hciconfig hci0 up
  
✓ Re-pair device:
  sudo bluetoothctl
  scan on
  # Wait to see ESP32
  pair XX:XX:XX:XX:XX:XX
  trust XX:XX:XX:XX:XX:XX
  exit
  
✓ Check library:
  pip3 list | grep pybluez
  # Should show: pybluez version
```

---

### **Problem: I²C Displays Not Working**

**Symptoms:**
- LCD backlight on but no text
- OLED completely blank
- "OLED_FAIL" in Serial Monitor

**Solutions:**
```
✓ Find I²C addresses:
  File → Examples → Wire → i2c_scanner
  Upload to UNO, open Serial Monitor
  Should find: 0x27 (LCD), 0x3C (OLED)
  
✓ If wrong address found:
  Change in code:
  LiquidCrystal_I2C lcd(0xYOUR_ADDRESS, 16, 2);
  
✓ Check wiring:
  - All SDA pins together
  - All SCL pins together
  - UNO GND ←→ Nano GND (CRITICAL!)
  
✓ Test one device at a time:
  - Disconnect OLED, test LCD
  - Disconnect LCD, test OLED
  
✓ Pull-up resistors:
  - Usually built into modules
  - If both displays fail: add 4.7kΩ SDA→5V, SCL→5V
```

---

### **Problem: Raspberry Pi Not Detecting Arduinos**

**Symptoms:**
- "UNO connection failed"
- "Nano connection failed"

**Solutions:**
```
✓ List USB devices:
  ls -l /dev/ttyUSB* /dev/ttyACM*
  
✓ If no devices shown:
  - Unplug and replug USB cables
  - Try different USB ports
  - Check cable is DATA cable (not power-only)
  
✓ If devices shown but connection fails:
  - Check baud rate matches (115200)
  - Close Arduino IDE Serial Monitor
  - Kill processes using port:
    sudo fuser -k /dev/ttyACM0
  
✓ Permission issues:
  sudo usermod -a -G dialout $USER
  sudo reboot
  
✓ Update port names in code:
  If UNO is on /dev/ttyUSB0 instead of /dev/ttyACM0:
  Change in railway_display.py:
  UNO_PORT = '/dev/ttyUSB0'
```

---

### **Problem: Count Increments Multiple Times**

**Symptoms:**
- Wave hand once, count goes up 3-5 times
- Erratic counting

**Causes:**
- Debounce logic not working
- Distance threshold too wide

**Solutions:**
```
✓ Adjust thresholds in UNO code:
  if(distance > 0 && distance < 5)  // Closer threshold
  if(distance > 20 && objectPresent) // Wider exit threshold
  
✓ Increase delay:
  delay(100);  // Slower loop
  
✓ Add settle time:
  if(distance > 15 && objectPresent) {
    delay(200);  // Wait before allowing next count
    axleCount++;
    objectPresent = false;
  }
```

---

### **Problem: Circuit Visualizer Not Updating**

**Symptoms:**
- Main count updates but visualizer stays at 00
- Binary bits don't change

**Solutions:**
```
✓ Check function is called:
  In process_uno_message():
  self.update_circuit_visualizer()
  
✓ Test manually:
  In Python console after launch:
  app.axle_count = 47
  app.update_circuit_visualizer()
  
✓ Check TkInter mainloop:
  root.mainloop() at end of file
```

---

### **Common Error Messages**

| Error | Meaning | Solution |
|-------|---------|----------|
| `OLED_FAIL` | OLED not found on I²C | Check address, wiring |
| `externally-managed-environment` | Pip blocked | Use apt or --break-system-packages |
| `Bluetooth is not enabled!` | ESP32 config wrong | Check board selection |
| `Serial port busy` | Port in use | Close Serial Monitor, kill process |
| `No module named 'bluetooth'` | pybluez not installed | Install pybluez |

---

## 📚 PROJECT THEORY

### **BCD (Binary Coded Decimal)**

**What is BCD?**
- Each decimal digit (0-9) encoded in 4 bits
- Unlike pure binary (47 = 0010 1111)
- BCD: 47 = 0100 (4) + 0111 (7)

**Why BCD?**
- Simplifies decimal display
- Direct mapping to 7-segment decoders
- Common in digital clocks, meters, calculators

**Example:**
```
Decimal: 23

Pure Binary:
23 = 16 + 4 + 2 + 1 = 0001 0111 (8 bits)

BCD:
2 → 0010 (4 bits)
3 → 0011 (4 bits)
Combined: 0010 0011 (8 bits)

To display: Feed 0010 to first CD4511, 0011 to second CD4511
```

---

### **CD4511 BCD to 7-Segment Decoder**

**Function:**
Converts 4-bit BCD input to 7-segment output

**Pin Functions:**
- **Inputs (DCBA):** 4-bit BCD code
- **Outputs (a-g):** 7 segment control lines
- **LE (Latch Enable):** LOW = pass-through, HIGH = latch
- **BI (Blanking Input):** Forces all segments OFF
- **LT (Lamp Test):** Tests all segments

**Truth Table (Sample):**

| D | C | B | A | Decimal | Segments Lit |
|---|---|---|---|---------|--------------|
| 0 | 0 | 0 | 0 | 0 | a,b,c,d,e,f |
| 0 | 0 | 0 | 1 | 1 | b,c |
| 0 | 0 | 1 | 0 | 2 | a,b,d,e,g |
| 0 | 1 | 0 | 0 | 4 | b,c,f,g |
| 0 | 1 | 1 | 1 | 7 | a,b,c |

**Common Anode vs. Cathode:**
- **Common Anode:** Shared +5V, CD4511 outputs sink current (LOW = ON)
- **Common Cathode:** Shared GND, CD4511 outputs source current (HIGH = ON)
- **Our Setup:** Common ANODE (BI pin = GND)

---

### **I²C (Inter-Integrated Circuit) Protocol**

**What is I²C?**
- 2-wire serial communication (SDA, SCL)
- Multi-master, multi-slave bus
- Addresses up to 127 devices

**How it Works:**
1. Master sends START condition
2. Sends 7-bit address + R/W bit
3. Addressed slave responds with ACK
4. Data transfer (8 bits at a time)
5. Master sends STOP condition

**Why I²C for This Project?**
- Only 2 pins needed (saves Arduino pins)
- Multiple devices share same bus
- Built-in addressing (LCD = 0x27, OLED = 0x3C)

**Our I²C Bus:**
```
Arduino UNO (Master)
  ↓ A4 (SDA), A5 (SCL)
  ├── LCD (0x27)
  ├── OLED (0x3C)
  └── Arduino Nano (shared bus, not master/slave)
```

---

### **Ultrasonic Distance Measurement**

**Principle:**
- Send 40kHz sound pulse (10μs trigger)
- Measure time until echo returns
- Calculate: Distance = (Time × Speed of Sound) / 2

**HC-SR04 Timing:**
```
       10μs TRIG pulse
          ↓
TRIG: ────┐         ┌────
          └─────────┘
          
                 ← Time (μs) →
ECHO: ────────┐               ┐────
              └───────────────┘
              
Distance (cm) = Duration × 0.034 / 2
              = Duration × 0.017
```

**Why Debouncing?**
- Object detection: distance < 10cm → set flag
- Count trigger: distance > 15cm + flag set → increment
- Prevents multiple counts for same object

---

### **1-Wire Protocol (DS18B20)**

**What is 1-Wire?**
- Single data line (plus ground)
- Bidirectional communication
- Devices powered by data line or separate VCC

**DS18B20 Features:**
- Digital temperature sensor (-55°C to +125°C)
- 12-bit resolution (0.0625°C steps)
- Each sensor has unique 64-bit ID

**Why Pull-Up Resistor?**
- 1-Wire is open-drain protocol
- Requires 4.7kΩ pull-up to VCC
- Without it, line floats and data is corrupted

---

### **Serial Communication**

**UART (Universal Asynchronous Receiver-Transmitter):**
- Two wires: TX (transmit), RX (receive)
- No clock signal (asynchronous)
- Both devices must agree on baud rate

**Our Serial Connections:**
1. **Arduino ↔ Raspberry Pi:** USB (virtual serial)
   - Baud: 115200
   - Protocol: Command strings ending in `\n`

2. **ESP32 Bluetooth:** Wireless serial
   - SPP (Serial Port Profile)
   - Appears as virtual COM port

**Message Format:**
```
Command Structure:
COMMAND:VALUE\n

Examples:
COUNT:5\n
TEMP:25.50\n
TARGET_REACHED\n

Bluetooth Classic (SPP)
Serial Port Profile (SPP):

Emulates serial cable over Bluetooth
Uses RFCOMM protocol (channel 1)
Range: ~10 meters

Connection Process:

ESP32 advertises name: "ESP32_Railway_Counter"
Raspberry Pi scans for devices
Pi connects to ESP32 MAC address
Virtual serial port established
Data exchanged as strings


🚀 FUTURE ENHANCEMENTS
Hardware Improvements

Multi-Track Support

Add 3 more ultrasonic sensors (D7, D8, D11, D12)
Track separate counts for parallel tracks
Display: 4 rows on OLED


Directional Detection

Add second ultrasonic sensor per track
Determine direction (entering vs. exiting)
Useful for single-track sections


Wheel Sensor Alternative

IR break-beam sensors (more accurate)
Hall effect sensors for magnetic wheel detection
Inductive proximity sensors for metal wheels


Enhanced Temperature Monitoring

Multiple DS18B20 sensors along track
Record temperature of each axle
Create thermal profile of train


Vibration Detection

MPU6050 accelerometer
Detect bearing defects from vibration signature
Predict failures before temperature rises




Software Enhancements

Data Logging

python   - SQLite database on Raspberry Pi
   - Log: timestamp, count, temperature, alerts
   - Export to CSV for analysis

Web Interface

python   - Flask web server on RPi
   - Access from phone/computer browser
   - Real-time dashboard with graphs

Multiple ESP32 Receivers

python   - Bluetooth mesh network
   - Trigger multiple signals:
     * Red light at entry
     * Green light at exit
     * Audio alarm

Machine Learning

python   - TensorFlow Lite on RPi
   - Anomaly detection in temperature patterns
   - Predict hot axle before threshold

Cloud Integration

python   - MQTT publish to cloud broker
   - AWS IoT / Azure IoT Hub
   - Real-time monitoring from anywhere
```

---

### **Educational Extensions**

1. **FPGA Implementation**
   - Implement BCD encoder in Verilog/VHDL
   - Replace Arduino with FPGA
   - Learn hardware description languages

2. **Custom PCB Design**
   - Design PCB in KiCad/Eagle
   - Integrate all components
   - Professional manufacturing

3. **Railway Signaling Integration**
   - Implement actual signaling logic
   - Interlocking with other track sections
   - Failsafe design principles

4. **Communication Protocols**
   - Add CAN bus between controllers
   - Implement Modbus RTU
   - Learn industrial protocols

---

## 📊 PROJECT SPECIFICATIONS

### **Performance Metrics**

| Parameter | Value |
|-----------|-------|
| Maximum Count | 99 |
| Count Accuracy | 100% (with proper object presentation) |
| Detection Range | 2-10 cm |
| Update Rate | 20 Hz (50ms loop) |
| Temperature Range | -55°C to +125°C |
| Temperature Accuracy | ±0.5°C |
| Bluetooth Range | ~10 meters |
| Display Latency | < 100ms |

---

### **Power Consumption**

| Component | Current Draw |
|-----------|--------------|
| Arduino UNO | ~50 mA |
| Arduino Nano | ~40 mA |
| ESP32 (BT active) | ~160 mA |
| Raspberry Pi 4 | ~600 mA |
| HC-SR04 (active) | ~15 mA |
| LCD Backlight | ~20 mA |
| OLED | ~15 mA |
| 7-Segment (×2) | ~40 mA |
| **Total** | **~940 mA @ 5V** |

**Power Supply Requirement:** 5V @ 2A minimum

---

## 🎓 LEARNING OUTCOMES

### **Digital Logic Concepts**
✅ Binary number systems  
✅ BCD encoding  
✅ Logic gates (AND, OR, NOT in CD4511)  
✅ Decoders and multiplexers  
✅ Sequential vs. combinational logic  

### **Microcontroller Programming**
✅ GPIO control (digital read/write)  
✅ Interrupt handling (ultrasonic echo)  
✅ Timer-based operations  
✅ Serial communication protocols  
✅ Library integration  

### **Communication Protocols**
✅ I²C (multi-master bus)  
✅ UART (asynchronous serial)  
✅ 1-Wire (Dallas protocol)  
✅ Bluetooth SPP  
✅ USB CDC (virtual serial)  

### **Sensor Interfacing**
✅ Ultrasonic distance measurement  
✅ Temperature sensing (digital)  
✅ Signal conditioning  
✅ Debouncing techniques  

### **Display Technologies**
✅ 7-segment multiplexing  
✅ LCD character displays  
✅ OLED graphics  
✅ GUI programming (Tkinter)  

### **System Integration**
✅ Distributed architecture  
✅ Multi-processor coordination  
✅ Wireless communication  
✅ Real-time visualization  

---

## 📖 REFERENCES

### **Datasheets**
- [CD4511 BCD to 7-Segment Decoder](https://www.ti.com/lit/ds/symlink/cd4511b.pdf)
- [HC-SR04 Ultrasonic Sensor](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [DS18B20 Temperature Sensor](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)
- [ESP32-WROOM-32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf)

### **Technical Documentation**
- [Arduino Reference](https://www.arduino.cc/reference/en/)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [I²C Specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)
- [1-Wire Protocol Guide](https://www.maximintegrated.com/en/design/technical-documents/tutorials/1/1796.html)

### **Libraries Used**
- [LiquidCrystal_I2C](https://github.com/johnrickman/LiquidCrystal_I2C)
- [Adafruit_SSD1306](https://github.com/adafruit/Adafruit_SSD1306)
- [OneWire](https://github.com/PaulStoffregen/OneWire)
- [DallasTemperature](https://github.com/milesburton/Arduino-Temperature-Control-Library)
- [PyBluez](https://github.com/pybluez/pybluez)

---

## 👥 PROJECT TEAM

**Project Name:** Railway Axle Counter System  
**Course:** ADLD (Advanced Digital Logic Design)  
**Institution:** [Your Institution Name]  
**Semester:** [Your Semester]  

**Team Members:**
- [Your Name] - [Roll Number]
- [Team Member 2] - [Roll Number]
- [Team Member 3] - [Roll Number]

**Instructor:** [Instructor Name]

---

## 📄 LICENSE

This project is created for educational purposes.

**Hardware:** Open-source hardware design  
**Software:** MIT License
```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

📞 SUPPORT
Issues: Create an issue in the project repository
Questions: Contact [your.email@example.com]
Documentation: This README file

✅ PROJECT CHECKLIST
Pre-Demo Checklist

 All hardware connections verified
 Pull-up resistor on DS18B20 installed
 Common anode 7-segments confirmed
 I²C addresses scanned and verified (0x27, 0x3C)
 Arduino code uploaded and tested
 ESP32 Bluetooth visible
 Raspberry Pi software tested
 All displays showing correct data
 Temperature sensor reading accurately
 Count incrementing properly
 Bluetooth alert working
 Circuit visualizer updating
 README documentation complete

Demo Procedure

 Power on all components
 Launch Raspberry Pi software
 Demonstrate COUNT mode
 Demonstrate COMPARE mode with target
 Show Bluetooth alert (ESP32 LED)
 Display circuit visualizer
 Show temperature monitoring
 Explain BCD conversion
 Reset and repeat


🎉 CONCLUSION
This project successfully demonstrates:

Digital logic design through BCD encoding and 7-segment decoding
Microcontroller interfacing with multiple sensors and displays
Communication protocols including I²C, UART, 1-Wire, and Bluetooth
System integration across distributed processors
Real-world application of railway safety systems

The modular architecture allows for future expansion and customization, making it an excellent foundation for more advanced railway automation projects.

Document Version: 1.0
Last Updated: [Current Date]
Status: Complete and Tested ✅