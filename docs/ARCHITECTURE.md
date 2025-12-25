# System Architecture and Workflow

## System Overview

The Smart Trash AIOT system is a modular AI-powered waste management solution that combines:
- **Computer Vision** for waste classification
- **Voice Recognition** for hands-free control
- **IoT Sensors** for automatic detection
- **Motor Control** for automatic lid operation

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  Smart Trash Controller                     │
│                        (main.py)                            │
└────────┬──────────────────────────────────────────┬─────────┘
         │                                          │
    ┌────▼────┐                                ┌────▼─────┐
    │ Inputs  │                                │ Outputs  │
    └────┬────┘                                └────┬─────┘
         │                                          │
    ┌────▼──────────────────────┐        ┌─────────▼──────────┐
    │  Input Modules            │        │  Output Modules    │
    ├───────────────────────────┤        ├────────────────────┤
    │                           │        │                    │
    │  ┌──────────────────┐    │        │  ┌──────────────┐ │
    │  │  Camera Module   │    │        │  │ Motor Control│ │
    │  │  - USB Camera    │    │        │  │ - Servo      │ │
    │  │  - Pi Camera     │    │        │  │ - Lid Open/  │ │
    │  └──────────────────┘    │        │  │   Close      │ │
    │                           │        │  └──────────────┘ │
    │  ┌──────────────────┐    │        │                    │
    │  │ Voice Recognition│    │        │  ┌──────────────┐ │
    │  │ - Microphone     │    │        │  │ Text-to-     │ │
    │  │ - Speech-to-Text │    │        │  │ Speech       │ │
    │  └──────────────────┘    │        │  │ - Voice      │ │
    │                           │        │  │   Feedback   │ │
    │  ┌──────────────────┐    │        │  └──────────────┘ │
    │  │ Ultrasonic Sensor│    │        │                    │
    │  │ - HC-SR04        │    │        │  ┌──────────────┐ │
    │  │ - Distance       │    │        │  │ Logging      │ │
    │  │   Measurement    │    │        │  │ - System Log │ │
    │  └──────────────────┘    │        │  │ - Events     │ │
    │                           │        │  └──────────────┘ │
    └───────────────────────────┘        └────────────────────┘
                │
                │
    ┌───────────▼────────────┐
    │  AI Processing Module  │
    ├────────────────────────┤
    │  Image Classifier      │
    │  - TensorFlow/Keras    │
    │  - CNN Model           │
    │  - 4 Categories:       │
    │    • Recyclable        │
    │    • Organic           │
    │    • Hazardous         │
    │    • General           │
    └────────────────────────┘
```

## Data Flow

### 1. Automatic Mode Workflow

```
┌─────────────────────┐
│  System Started     │
│  Main Loop Running  │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│ Ultrasonic Sensor    │
│ Continuously Scanning│
└──────────┬───────────┘
           │
           │ Object Detected
           │ (Distance < 30cm)
           ▼
┌──────────────────────┐
│  Auto Open Lid       │
│  (Servo Motor)       │
└──────────┬───────────┘
           │
           │ Wait 1 second
           ▼
┌──────────────────────┐
│  Capture Image       │
│  (Camera Module)     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  AI Classification   │
│  (Image Classifier)  │
└──────────┬───────────┘
           │
           │ Result: Category + Confidence
           ▼
┌──────────────────────┐
│  Voice Feedback      │
│  "Rác có thể tái chế"│
└──────────┬───────────┘
           │
           │ Wait 5 seconds
           ▼
┌──────────────────────┐
│  Auto Close Lid      │
│  (Servo Motor)       │
└──────────┬───────────┘
           │
           ▼
     [Loop Back]
```

### 2. Voice Command Workflow

```
┌─────────────────────┐
│  User Speaks        │
│  "Mở nắp"           │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│ Voice Recognition    │
│ Listen & Recognize   │
└──────────┬───────────┘
           │
           │ Text: "mở nắp"
           ▼
┌──────────────────────┐
│  Command Parser      │
│  Match Keywords      │
└──────────┬───────────┘
           │
           │ Command: "open"
           ▼
┌──────────────────────┐
│  Execute Command     │
│  - open_lid()        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Voice Feedback      │
│  "Đã mở nắp"        │
└──────────────────────┘
```

### 3. Manual Classification Workflow

```
┌─────────────────────┐
│ User Command:       │
│ "Phân loại"         │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│  Capture Image       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  AI Classification   │
└──────────┬───────────┘
           │
           │ Result
           ▼
┌──────────────────────┐
│  Speak Result        │
│  "Recyclable, 85%    │
│   confidence"        │
└──────────────────────┘
```

## Module Responsibilities

### SmartTrashController (Main)
- **Responsibility**: Orchestrate all modules
- **Functions**:
  - Initialize all subsystems
  - Main control loop
  - Event handling
  - Resource cleanup

### Image Processing Module
- **Responsibility**: Visual analysis
- **Functions**:
  - Camera management
  - Image capture
  - AI-based classification
  - Fallback color-based classification

### Voice Recognition Module
- **Responsibility**: Audio interaction
- **Functions**:
  - Speech-to-text conversion
  - Command parsing
  - Text-to-speech feedback
  - Multi-language support

### Motor Control Module
- **Responsibility**: Physical actuation
- **Functions**:
  - Servo motor control
  - Lid opening/closing
  - PWM signal generation
  - GPIO management

### Sensor Module
- **Responsibility**: Environment detection
- **Functions**:
  - Distance measurement
  - Object detection
  - Trigger automation

## Configuration System

The system uses YAML-based configuration for flexibility:

```
config.yaml
    ↓
load_config()
    ↓
Configuration Dictionary
    ↓
Passed to each module during initialization
```

## Error Handling

```
Module Initialization
    ├─ Success → Continue
    └─ Failure → Log warning + Continue with degraded functionality

Hardware Access
    ├─ GPIO Available → Use real hardware
    └─ GPIO Not Available → Use simulation mode

AI Model
    ├─ Model Exists → Load and use
    └─ No Model → Use fallback color-based classifier

Network (Voice Recognition)
    ├─ Internet Available → Use Google API
    └─ No Internet → Timeout and continue
```

## Extensibility

The modular design allows easy extensions:

### Add New Waste Categories
1. Update `config.yaml` with new categories
2. Train model with new classes
3. Add voice feedback translations

### Add New Commands
1. Add keywords to `config.yaml`
2. Implement handler in `SmartTrashController`
3. Add voice feedback

### Add New Sensors
1. Create sensor class in `motor_control.py`
2. Initialize in `SmartTrashController`
3. Add to main control loop

### Add Remote Monitoring
1. Add IoT module (MQTT, HTTP)
2. Send events to cloud
3. Enable remote control

## Performance Considerations

### Raspberry Pi Optimization
- Use TensorFlow Lite for faster inference
- Reduce image resolution if needed
- Adjust sensor polling frequency
- Optimize main loop sleep duration

### Resource Management
- Camera: Release when not in use
- GPIO: Cleanup on exit
- Memory: Use efficient image processing
- CPU: Balance between responsiveness and power

## Security Considerations

### Physical Security
- Secure GPIO connections
- Protect camera from tampering
- Weatherproof enclosure

### Software Security
- Input validation on voice commands
- Sanitize file paths
- Limit GPIO access
- Secure configuration files

### Privacy
- Local processing (no cloud image upload)
- Optional voice recording logging
- Clear data retention policy
