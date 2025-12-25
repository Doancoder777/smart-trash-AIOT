# Installation Guide - Hướng dẫn Cài đặt

## Requirements - Yêu cầu

### Hardware - Phần cứng
- **Raspberry Pi 3/4** (khuyến nghị) hoặc máy tính có camera
- **Camera**: USB camera hoặc Raspberry Pi Camera Module
- **Microphone**: USB microphone
- **Servo Motor**: SG90 hoặc MG90S
- **Ultrasonic Sensor**: HC-SR04
- **Power Supply**: 5V/3A cho Raspberry Pi

### Software - Phần mềm
- **Python**: 3.8 hoặc cao hơn
- **Operating System**: Raspberry Pi OS, Ubuntu Linux, Windows 10/11, macOS

## Installation - Cài đặt

### 1. Clone Repository

```bash
git clone https://github.com/Doancoder777/smart-trash-AIOT.git
cd smart-trash-AIOT
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### 3. Configure

Edit `config.yaml` to match your hardware setup.

### 4. Run

```bash
./start.sh
# or
cd src && python main.py
```

For complete installation guide, see full documentation.
