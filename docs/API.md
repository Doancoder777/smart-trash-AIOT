# API Reference

## SmartTrashController

Main controller class that integrates all modules.

### Constructor

```python
SmartTrashController(config_path: str = "config.yaml")
```

### Methods

#### `initialize_modules() -> bool`
Initialize all system modules (camera, classifier, voice, motor, sensor).

**Returns:** `True` if all modules initialized successfully.

#### `classify_waste() -> tuple`
Capture image and classify waste.

**Returns:** Tuple of `(category, confidence)`

#### `handle_voice_command(command: str)`
Handle voice command.

**Parameters:**
- `command`: Command name ('open', 'close', 'classify', 'status')

#### `open_lid()`
Open the trash bin lid.

#### `close_lid()`
Close the trash bin lid.

#### `run()`
Start the main control loop.

#### `cleanup()`
Cleanup all resources.

---

## ImageClassifier

AI-powered image classifier for waste categorization.

### Constructor

```python
ImageClassifier(model_path: str, categories: list, confidence_threshold: float = 0.7)
```

### Methods

#### `classify(image: np.ndarray) -> Tuple[str, float]`
Classify waste in the image.

**Parameters:**
- `image`: Input image as numpy array

**Returns:** Tuple of `(category, confidence)`

---

## CameraModule

Camera module for capturing images.

### Constructor

```python
CameraModule(device_id: int = 0, resolution: Tuple[int, int] = (640, 480))
```

### Methods

#### `initialize() -> bool`
Initialize camera connection.

#### `capture_image() -> Optional[np.ndarray]`
Capture a single image from camera.

**Returns:** Captured image or None if failed

#### `release()`
Release camera resources.

---

## VoiceRecognition

Voice recognition module for processing voice commands.

### Constructor

```python
VoiceRecognition(language: str = "vi-VN", timeout: int = 5, 
                 phrase_time_limit: int = 3, commands: dict = None)
```

### Methods

#### `initialize() -> bool`
Initialize microphone.

#### `listen() -> Optional[str]`
Listen for voice command.

**Returns:** Recognized text or None if failed

#### `parse_command(text: str) -> Optional[str]`
Parse text to identify command.

**Returns:** Command name or None if no match

#### `speak(text: str)`
Speak text using text-to-speech.

#### `get_voice_feedback(category: str, language: str = "vi") -> str`
Get voice feedback message for waste category.

---

## MotorController

Motor controller for lid operation.

### Constructor

```python
MotorController(motor_pin: int, min_angle: int = 0, max_angle: int = 90)
```

### Methods

#### `initialize() -> bool`
Initialize GPIO and PWM.

#### `open_lid()`
Open the trash bin lid.

#### `close_lid()`
Close the trash bin lid.

#### `cleanup()`
Cleanup GPIO resources.

---

## UltrasonicSensor

Ultrasonic sensor for distance measurement.

### Constructor

```python
UltrasonicSensor(trigger_pin: int, echo_pin: int, threshold: float = 30.0)
```

### Methods

#### `initialize() -> bool`
Initialize GPIO pins.

#### `measure_distance() -> Optional[float]`
Measure distance in centimeters.

**Returns:** Distance in cm or None if failed

#### `is_object_detected() -> bool`
Check if object is within threshold distance.

---

## Utility Functions

### `load_config(config_path: str = "config.yaml") -> Dict[str, Any]`
Load configuration from YAML file.

### `setup_logging(log_file: str = None, level: int = logging.INFO)`
Setup logging configuration.

### `ensure_directories()`
Ensure required directories exist.

---

## Configuration

The system uses a YAML configuration file (`config.yaml`) with the following structure:

```yaml
camera:
  resolution: [640, 480]
  fps: 30
  device_id: 0

classification:
  model_path: "models/waste_classifier.h5"
  confidence_threshold: 0.7
  categories:
    - recyclable
    - organic
    - hazardous
    - general

voice:
  language: "vi-VN"
  timeout: 5
  phrase_time_limit: 3
  commands:
    open: ["mở nắp", "mở", "open"]
    close: ["đóng nắp", "đóng", "close"]
    classify: ["phân loại", "classify", "nhận diện"]
    status: ["trạng thái", "status"]

motor:
  lid_motor_pin: 17
  servo_min_angle: 0
  servo_max_angle: 90
  open_duration: 3

sensors:
  ultrasonic_trigger_pin: 23
  ultrasonic_echo_pin: 24
  distance_threshold: 30

system:
  auto_close_delay: 5
  voice_feedback: true
  log_file: "logs/smart_trash.log"
```
