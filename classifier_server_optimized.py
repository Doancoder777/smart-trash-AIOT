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
TEMP_IMAGE_DIR = "temp_images"
ESP32_IP = '192.168.1.101' # <--- IP ESP32 CỦA BẠN

# Bảng mã thùng rác
LABEL_TO_BIN_ID = {
    "bio": "1",
    "battery": "2", "glass": "2", "metal": "2", "plastic": "2", "plastic_bag": "2",
    "cardboard": "3", "paper": "3", "cloth": "3", "shoe": "2", "trash": "2"
}

# --- KHỞI TẠO (CHẠY 1 LẦN) ---
torch.set_num_threads(4) 
if not os.path.exists(TEMP_IMAGE_DIR): os.makedirs(TEMP_IMAGE_DIR)

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

# --- KHỞI ĐỘNG CAMERA (QUAN TRỌNG: Mở sẵn ở ngoài vòng lặp) ---
print("📷 Đang khởi động Webcam (Chờ xíu)...")
cap = cv2.VideoCapture(0)
# Tối ưu buffer để lấy ảnh mới nhất
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) 

if not cap.isOpened():
    print("❌ LỖI: Không mở được Webcam!")
    sys.exit()
print("✅ Webcam đã sẵn sàng!")

# --- CÁC HÀM XỬ LÝ ---
def send_open_command(bin_id, target_addr):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        command_str = f"OPEN:{bin_id}" 
        sock.sendto(command_str.encode('utf-8'), (ESP32_IP, UDP_PORT)) # Gửi thẳng đến IP cố định
        print(f"📡 Đã gửi lệnh: **{command_str}**")
        sock.close()
    except Exception as e:
        print(f"❌ Lỗi gửi UDP: {e}")

def capture_and_process():
    # Xả buffer cũ để lấy ảnh mới nhất (quan trọng khi cam bật liên tục)
    # Đọc bỏ 1-2 frame cũ đang chờ trong hàng đợi
    cap.grab() 
    
    # Chụp ảnh thật (Lấy frame mới nhất)
    ret, frame = cap.read()

    if not ret:
        print("❌ Lỗi đọc Frame.")
        return

    # Xử lý AI ngay lập tức
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
    send_open_command(bin_id, (ESP32_IP, UDP_PORT))
    print("-" * 30)

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(SERVER_ADDRESS)
        print(f"🚀 SERVER ĐANG LẮNG NGHE UDP TẠI: {SERVER_ADDRESS}")
    except Exception as e:
        print(f"❌ Lỗi Server: {e}")
        return

    while True:
        try:
            # Lắng nghe Trigger từ ESP32
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8').strip()
            
            if message == "TRIGGER_CAMERA":
                print(f"\n📸 [EVENT] Nhận Trigger -> Xử lý ngay!")
                capture_and_process()
            else:
                print(f"📩 Tin lạ: {message}")
                
        except KeyboardInterrupt:
            print("\n👋 Dừng chương trình.")
            break
        except Exception as e:
            print(f"⚠️ Lỗi: {e}")
    
    # Dọn dẹp khi tắt
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()