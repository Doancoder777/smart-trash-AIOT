# Smart Trash AIOT 🗑️🤖

Thùng rác thông minh tích hợp trí tuệ nhân tạo xử lý ảnh và giọng nói hỗ trợ phân loại rác thải đóng mở tự động.

**Smart Trash Bin with AI-powered image and voice processing for automatic waste classification and lid control.**

## Tính năng / Features

### 🎯 Phân loại rác tự động bằng AI
- Sử dụng camera để chụp ảnh rác thải
- Phân loại rác thành 4 loại: Tái chế, Hữu cơ, Nguy hại, Thông thường
- Độ chính xác cao với mô hình deep learning

### 🗣️ Điều khiển bằng giọng nói
- Nhận diện giọng nói tiếng Việt và tiếng Anh
- Các lệnh: "mở nắp", "đóng nắp", "phân loại", "trạng thái"
- Phản hồi bằng giọng nói

### 🚪 Đóng mở tự động
- Cảm biến siêu âm phát hiện đối tượng
- Tự động mở nắp khi có người đến gần
- Tự động đóng sau khoảng thời gian cài đặt

### 🤖 Tích hợp IoT
- Hỗ trợ Raspberry Pi
- Điều khiển động cơ servo
- Ghi log hoạt động

## Kiến trúc hệ thống / System Architecture

```
Smart Trash AIOT
├── src/
│   ├── main.py                    # Main controller
│   ├── modules/
│   │   ├── image_processing.py    # AI image classification
│   │   ├── voice_recognition.py   # Voice command processing
│   │   └── motor_control.py       # Motor & sensor control
│   └── utils/
│       └── helpers.py             # Utility functions
├── models/                         # AI models
├── logs/                          # System logs
├── config.yaml                    # Configuration file
└── requirements.txt               # Dependencies
```

## Cài đặt / Installation

### Yêu cầu hệ thống / Requirements
- Python 3.8+
- Raspberry Pi (khuyến nghị / recommended) hoặc máy tính có camera
- Camera USB hoặc Pi Camera
- Microphone
- Servo motor (cho Raspberry Pi)
- Cảm biến siêu âm HC-SR04 (tùy chọn / optional)

### Cài đặt thư viện / Install Dependencies

```bash
# Clone repository
git clone https://github.com/Doancoder777/smart-trash-AIOT.git
cd smart-trash-AIOT

# Tạo môi trường ảo / Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc / or
venv\Scripts\activate  # Windows

# Cài đặt các thư viện / Install dependencies
pip install -r requirements.txt
```

### Cấu hình / Configuration

Chỉnh sửa file `config.yaml` để cấu hình hệ thống:

```yaml
# Camera settings
camera:
  resolution: [640, 480]
  device_id: 0

# Voice recognition
voice:
  language: "vi-VN"  # Vietnamese
  
# Motor control (GPIO pins for Raspberry Pi)
motor:
  lid_motor_pin: 17
  
# Sensors
sensors:
  ultrasonic_trigger_pin: 23
  ultrasonic_echo_pin: 24
  distance_threshold: 30  # cm
```

## Sử dụng / Usage

### Chạy hệ thống / Run the system

```bash
cd src
python main.py
```

### Lệnh giọng nói / Voice Commands

**Tiếng Việt:**
- "Mở nắp" - Mở nắp thùng rác
- "Đóng nắp" - Đóng nắp thùng rác
- "Phân loại" - Phân loại rác thải
- "Trạng thái" - Kiểm tra trạng thái

**English:**
- "Open" - Open the lid
- "Close" - Close the lid
- "Classify" - Classify waste
- "Status" - Check status

### Chế độ tự động / Automatic Mode

Hệ thống tự động:
1. Phát hiện đối tượng qua cảm biến siêu âm
2. Mở nắp tự động
3. Chụp ảnh và phân loại rác
4. Thông báo kết quả bằng giọng nói
5. Tự động đóng sau 5 giây

## Kết nối phần cứng / Hardware Connection

### Raspberry Pi GPIO Pinout

```
Servo Motor:
- VCC    -> 5V
- GND    -> GND
- Signal -> GPIO 17 (default)

Ultrasonic Sensor (HC-SR04):
- VCC    -> 5V
- GND    -> GND
- Trigger -> GPIO 23 (default)
- Echo    -> GPIO 24 (default)

Camera:
- USB Camera hoặc Pi Camera Module

Microphone:
- USB Microphone
```

## Mô hình AI / AI Model

Hệ thống hỗ trợ mô hình phân loại rác sử dụng TensorFlow/Keras:

- Đặt file mô hình tại: `models/waste_classifier.h5`
- Mô hình phân loại 4 loại: recyclable, organic, hazardous, general
- Nếu không có mô hình, hệ thống sử dụng phân loại dựa trên màu sắc

### Huấn luyện mô hình / Training Model

Bạn có thể huấn luyện mô hình riêng với dataset của mình:

```python
# Example training code (not included)
# Train with waste classification dataset
# Save model to models/waste_classifier.h5
```

## Development

### Cấu trúc mã nguồn / Code Structure

- `main.py`: Controller chính tích hợp tất cả module
- `image_processing.py`: Xử lý ảnh và phân loại AI
- `voice_recognition.py`: Nhận diện và xử lý giọng nói
- `motor_control.py`: Điều khiển động cơ và cảm biến
- `helpers.py`: Các hàm tiện ích

### Testing

```bash
# Test camera
python -c "from modules.image_processing import CameraModule; cam = CameraModule(); cam.initialize(); print(cam.capture_image() is not None)"

# Test voice recognition
python -c "from modules.voice_recognition import VoiceRecognition; voice = VoiceRecognition(); voice.initialize(); print('Say something...'); print(voice.listen())"
```

## Troubleshooting

### Lỗi thường gặp / Common Issues

1. **Camera không hoạt động:**
   - Kiểm tra kết nối USB
   - Thay đổi `device_id` trong config.yaml
   - Kiểm tra quyền truy cập camera

2. **Microphone không nhận diện:**
   - Kiểm tra quyền microphone
   - Cài đặt PyAudio: `sudo apt-get install portaudio19-dev`
   - Test microphone với system tools

3. **GPIO errors trên Raspberry Pi:**
   - Chạy với quyền sudo: `sudo python main.py`
   - Kiểm tra kết nối GPIO
   - Cài đặt RPi.GPIO: `pip install RPi.GPIO`

4. **TensorFlow errors:**
   - Cài đặt phiên bản tương thích với hệ thống
   - Raspberry Pi: sử dụng TensorFlow Lite

## Đóng góp / Contributing

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## License

Dự án này được phát hành dưới giấy phép MIT License.

## Tác giả / Author

- GitHub: [@Doancoder777](https://github.com/Doancoder777)

## Liên hệ / Contact

Nếu có câu hỏi hoặc đề xuất, vui lòng tạo issue trên GitHub.

---

**Made with ❤️ for a cleaner environment 🌍**
