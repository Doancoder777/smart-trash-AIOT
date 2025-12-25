#include <WiFi.h>
#include <WiFiUdp.h>
#include <WebSocketMCP.h>
#include <ArduinoJson.h>
#include <string.h>
#include <ESP32Servo.h> // <--- 1. THÊM THƯ VIỆN SERVO

// --- CẤU HÌNH PIN SERVO ---
#define PIN_BIO 19        
#define PIN_NON_BURN 14   
#define PIN_BURN 5    

// --- CẤU HÌNH MẠNG ---
const char* ssid = "Ngoc Thoai";        
const char* password = "0934918347"; 
IPAddress laptopIP; 
bool isLaptopConnected = false; 
const int portUDP = 4210; 

// --- CẤU HÌNH XIAOZHI ---
const char* mcpEndpoint = "wss://api.xiaozhi.me/mcp/?token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjY5ODc1NSwiYWdlbnRJZCI6MTE5NzUyMSwiZW5kcG9pbnRJZCI6ImFnZW50XzExOTc1MjEiLCJwdXJwb3NlIjoibWNwLWVuZHBvaW50IiwiaWF0IjoxNzY1Nzc2NjE0LCJleHAiOjE3OTczMzQyMTR9.vdRFwpDBqCOE50cC_phGucXdb1rdtVDqMM4oP_jHJDsQGgTcClDgTWkBDHboaJUYDT5K0ovi54zHoUzj8lNa3Q";

#define TRIG_PIN 25
#define ECHO_PIN 35
#define DISTANCE_THRESHOLD 30 
#define STABLE_READS 2 

WebSocketMCP mcpClient; 
WiFiUDP Udp; 

// --- 2. KHAI BÁO SERVO ---
Servo bins[3]; // Tạo mảng 3 Servo cho gọn
int servoPins[3] = {PIN_BIO, PIN_NON_BURN, PIN_BURN};
unsigned long closeTime[3] = {0, 0, 0}; 
const char* binNames[3] = {"HUU CO", "KHONG DOT", "DOT DUOC"};
const int DEFAULT_TIME = 7; 

int consecutiveDetects = 0;
unsigned long lastTriggerTime = 0;
const int TRIGGER_COOLDOWN = 5000; 

// --- CÁC HÀM CẢM BIẾN (GIỮ NGUYÊN) ---
float getDistance() {
    digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    long duration = pulseIn(ECHO_PIN, HIGH, 30000); 
    if (duration == 0) return 999; 
    return duration * 0.034 / 2;
}

// --- 3. SỬA LOGIC ĐIỀU KHIỂN (SERVO) ---
void controlBinWithTimer(int id, int durationSec) {
    if (id < 1 || id > 3) return;
    int index = id - 1;
    
    Serial.println("--------------------------------");
    if (durationSec == -1) {
        // --- ĐÓNG: Quay về 0 độ ---
        bins[index].write(0); 
        closeTime[index] = 0; 
        Serial.printf("🔴 DONG NGAY (0 do) Thung %s\n", binNames[index]);
    } else {
        // --- MỞ: Quay ra 180 độ ---
        bins[index].write(180); 
        
        if (durationSec > 0) {
            closeTime[index] = millis() + (durationSec * 1000);
            Serial.printf("⏱️ MO (180 do, %ds) -> Tu dong dong: Thung %s\n", durationSec, binNames[index]);
        } else {
            closeTime[index] = 0;
            Serial.printf("🟢 MO LUON (180 do): Thung %s\n", binNames[index]);
        }
    }
    Serial.println("--------------------------------");
}

// --- CÁC HÀM MẠNG (GIỮ NGUYÊN) ---
void broadcastHandshake() {
    IPAddress broadcastIP(255, 255, 255, 255);
    const char* msg = "WHO_ARE_YOU_LAPTOP";
    Udp.beginPacket(broadcastIP, portUDP);
    Udp.write((const uint8_t*)msg, strlen(msg));
    Udp.endPacket();
    Serial.print("."); 
}

void sendUdpTrigger() {
    if (!isLaptopConnected) {
        Serial.println("⚠️ Chua ket noi Laptop, khong gui trigger!");
        return;
    }
    const char* msg = "TRIGGER_CAMERA";
    Udp.beginPacket(laptopIP, portUDP);
    Udp.write((const uint8_t*)msg, strlen(msg));
    Udp.endPacket();
    Serial.println(">>> [UDP] GUI LENH CHUP ANH >>>");
}

void checkUdpCommand() {
    int packetSize = Udp.parsePacket();
    if (packetSize) {
        char packet[30]; 
        int len = Udp.read(packet, 29);
        if (len > 0) packet[len] = 0;
        
        String cmd = String(packet);
        cmd.trim();
        
        if (cmd == "I_AM_LAPTOP") {
            laptopIP = Udp.remoteIP();
            isLaptopConnected = true;
            Serial.println("\n✅ DA TIM THAY LAPTOP!");
            Serial.print("💻 IP Laptop: "); Serial.println(laptopIP);
            return;
        }

        if (cmd.startsWith("OPEN:")) {
            int id = cmd.substring(5).toInt();
            Serial.printf("<< [UDP] Lenh mo thung: %d\n", id);
            controlBinWithTimer(id, DEFAULT_TIME); 
        }
    }
}

void registerMcpTools() {
    String desc = "Ma lenh: 11(Mo Bio), 10(Dong Bio), 21(Mo Non-Burn), 20(Dong Non-Burn), 31(Mo Burn), 30(Dong Burn)";
    String toolSchema = "{\"type\":\"object\",\"properties\":{\"code\":{\"type\":\"integer\",\"description\":\"" + desc + "\"}},\"required\":[\"code\"]}";

    mcpClient.registerTool("bin_ctrl", "Dieu khien thung rac", toolSchema, [](const String& args) {
        DynamicJsonDocument doc(256);
        DeserializationError error = deserializeJson(doc, args);
        if (error) { return WebSocketMCP::ToolResponse("{\"ok\":false}"); }
        
        int code = doc["code"];
        String msg = "OK";
        Serial.println("--------------------------------");
        Serial.print("📥 [MCP] Nhan lenh ma so: "); Serial.println(code);

        switch (code) {
            case 11: controlBinWithTimer(1, DEFAULT_TIME); msg = "Mo Bio 7s"; break;
            case 10: controlBinWithTimer(1, -1); msg = "Dong Bio"; break;
            case 21: controlBinWithTimer(2, DEFAULT_TIME); msg = "Mo Non-Burn 7s"; break;
            case 20: controlBinWithTimer(2, -1); msg = "Dong Non-Burn"; break;
            case 31: controlBinWithTimer(3, DEFAULT_TIME); msg = "Mo Burn 7s"; break;
            case 30: controlBinWithTimer(3, -1); msg = "Dong Burn"; break;
            default: msg = "Invalid Code"; break;
        }
        return WebSocketMCP::ToolResponse("{\"status\":\"" + msg + "\"}");
    });
}

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT); pinMode(ECHO_PIN, INPUT);
    
    // --- 4. KHỞI TẠO SERVO ---
    // ESP32Servo cần set Min/Max Pulse Width để hoạt động mượt
    // Thông số 500-2400 là chuẩn cho hầu hết servo SG90, MG996R
    for(int i=0; i<3; i++) {
        bins[i].attach(servoPins[i], 500, 2400); 
        bins[i].write(0); // Đảm bảo lúc khởi động là ĐÓNG
    }
    
    Serial.println("\n--- KHOI DONG ---");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    Serial.println("\n✅ Wifi OK (DHCP)");
    Serial.print("IP Address ESP32: "); Serial.println(WiFi.localIP());
    
    Udp.begin(portUDP);
    mcpClient.begin(mcpEndpoint, [](bool connected) {
        if(connected) registerMcpTools();
    });
}

void loop() {
    mcpClient.loop();
    checkUdpCommand();

    unsigned long now = millis();

    static unsigned long lastBroadcast = 0;
    if (!isLaptopConnected) {
        if (now - lastBroadcast > 2000) { 
            broadcastHandshake();
            lastBroadcast = now;
        }
    }

    // --- 5. LOGIC TỰ ĐỘNG ĐÓNG (CẬP NHẬT CHO SERVO) ---
    for(int i=0; i<3; i++) {
        if (closeTime[i] > 0 && now >= closeTime[i]) {
            bins[i].write(0); // <--- ĐÓNG SERVO (0 độ)
            closeTime[i] = 0; 
            Serial.printf("⏰ HET GIO -> Tu dong DONG Thung %s\n", binNames[i]);
        }
    }

    // --- CẢM BIẾN (GIỮ NGUYÊN) ---
    static unsigned long lastMeasure = 0;
    if (now - lastMeasure > 1000) { 
        lastMeasure = now;
        float dist = getDistance();
        
        if (dist > 0 && dist < DISTANCE_THRESHOLD) {
            consecutiveDetects++;
            if (consecutiveDetects >= STABLE_READS) { 
                if (now - lastTriggerTime > TRIGGER_COOLDOWN) {
                    sendUdpTrigger(); 
                    lastTriggerTime = now;
                    consecutiveDetects = 0;
                }
            }
        } else {
            consecutiveDetects = 0;
        }
    }
    delay(10);
}