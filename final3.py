import socket
import sys
import os
import time
from PIL import Image
import torch
import cv2 
from transformers import AutoImageProcessor, AutoModelForImageClassification

# ================= CẤU HÌNH =================
UDP_PORT = 4210
SERVER_IP = "0.0.0.0" 
SERVER_ADDRESS = (SERVER_IP, UDP_PORT)
MODEL_PATH = "." 

# --- THAY ĐỔI: KHÔNG CẤU HÌNH IP CỨNG ---
ESP32_IP = None # Sẽ tự động cập nhật khi ESP32 gọi
ESP32_PORT = UDP_PORT 

# Bảng mã thùng rác
LABEL_TO_BIN_ID = {
    "bio": "1",
    "battery": "2", "glass": "2", "metal": "2", "plastic": "2", "plastic_bag": "2",
    "cardboard": "3", "paper": "3", "cloth": "3", "shoe": "2", "trash": "2"
}

# --- KHỞI TẠO (GIỮ NGUYÊN) ---
torch.set_num_threads(4) 
print(f"⏳ Đang tải mô hình...")
if not os.path.exists(MODEL_PATH):
    print("❌ LỖI: Không tìm thấy model.")
    sys.exit()

try:
    processor = AutoImageProcessor.from_pretrained(MODEL_PATH)
    model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)
    model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    print("✅ AI SẴN SÀNG!")
except Exception as e:
    print(f"❌ Lỗi tải model: {e}")
    sys.exit()

# --- KHỞI ĐỘNG CAMERA (GIỮ NGUYÊN) ---
print("📷 Đang khởi động Webcam...")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) 
if not cap.isOpened():
    print("❌ LỖI: Không mở được Webcam!")
    sys.exit()
print("✅ Webcam đã sẵn sàng!")

# --- CÁC HÀM XỬ LÝ ---
def send_open_command(bin_id):
    global ESP32_IP
    if ESP32_IP is None:
        print("⚠️ Chưa tìm thấy ESP32, không thể gửi lệnh mở!")
        return

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        command_str = f"OPEN:{bin_id}" 
        sock.sendto(command_str.encode('utf-8'), (ESP32_IP, ESP32_PORT))
        print(f"📡 Đã gửi lệnh tới {ESP32_IP}: **{command_str}**")
        sock.close()
    except Exception as e:
        print(f"❌ Lỗi gửi UDP: {e}")

def capture_and_process():
    # (GIỮ NGUYÊN LOGIC CŨ)
    cap.grab() 
    ret, frame = cap.read()
    if not ret:
        print("❌ Lỗi đọc Frame.")
        return

    start_time = time.time()
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = image.resize((224, 224))
    
    inputs = processor(images=[image], return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    label = model.config.id2label[idx]
    score = logits.softmax(-1)[0, idx].item() * 100
    
    process_time = time.time() - start_time

    print("-" * 30)
    print(f"🧠 KẾT QUẢ: **{label.upper()}** ({score:.1f}%) | ⚡ Xử lý: {process_time:.3f}s")
    
    bin_id = LABEL_TO_BIN_ID.get(label, "2")
    send_open_command(bin_id)
    print("-" * 30)

def main():
    global ESP32_IP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(SERVER_ADDRESS)
        print(f"🚀 SERVER ĐANG LẮNG NGHE UDP TẠI: {SERVER_ADDRESS}")
        print("⏳ Đang đợi ESP32 kết nối...")
    except Exception as e:
        print(f"❌ Lỗi Server: {e}")
        return

    while True:
        try:
            # Lắng nghe Trigger từ ESP32
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8').strip()
            
            # --- LOGIC TỰ ĐỘNG TÌM IP ---
            if message == "WHO_ARE_YOU_LAPTOP":
                if ESP32_IP != addr[0]:
                    print(f"🔗 Đã tìm thấy ESP32 tại IP: {addr[0]}")
                    ESP32_IP = addr[0]
                
                # Phản hồi lại để ESP32 biết IP của Laptop
                response = "I_AM_LAPTOP"
                sock.sendto(response.encode('utf-8'), addr)
                
            elif message == "TRIGGER_CAMERA":
                # Cập nhật lại IP phòng trường hợp nó đổi mà không handshake lại
                ESP32_IP = addr[0] 
                print(f"\n📸 [EVENT] Nhận Trigger từ {addr[0]} -> Xử lý ngay!")
                capture_and_process()
            else:
                print(f"📩 Tin lạ từ {addr}: {message}")
                
        except KeyboardInterrupt:
            print("\n👋 Dừng chương trình.")
            break
        except Exception as e:
            print(f"⚠️ Lỗi: {e}")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()