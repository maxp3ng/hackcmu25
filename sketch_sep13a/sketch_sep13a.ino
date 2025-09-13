#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP udp;
char packetBuffer[255];
unsigned int localPort = 4800;
const char *ssid = "shado";
const char *password = "poopypoo";

// Frequency and resolution
int freq = 5000;          // 5 kHz PWM
int resolution = 8;       // 8-bit (0–255)
int check = 1;

IPAddress lastSenderIP;
unsigned int lastSenderPort = 0;
unsigned long lastKeepAlive = 0;
#define KEEPALIVE_INTERVAL 5000  // 5 seconds

void setupWifi() {
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(F("."));
  }
  udp.begin(localPort);
  Serial.printf("UDP server : %s:%i \n", WiFi.localIP().toString().c_str(), localPort);
}

void setup() {
  Serial.begin(115200);
  setupWifi();
}

void loopUDPServer() {
  int packetSize = udp.parsePacket();
  
  if (packetSize) {
    check++;
    int len = udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len - 1] = 0;
    
    lastSenderIP = udp.remoteIP();
    lastSenderPort = udp.remotePort();
    
    Serial.print("Received from: "); Serial.println(lastSenderIP);
    Serial.print("Size: "); Serial.println(packetSize);
    Serial.printf("Data: %s\n", packetBuffer);

    // Echo back immediately
    udp.beginPacket(lastSenderIP, lastSenderPort);
    udp.printf("UDP packet was received OK\r\n");
    udp.endPacket();
  }

  // Keepalive every KEEPALIVE_INTERVAL ms
  if (lastSenderPort && millis() - lastKeepAlive > KEEPALIVE_INTERVAL) {
    udp.beginPacket(lastSenderIP, lastSenderPort);
    udp.printf("KEEPALIVE");
    udp.endPacket();
    lastKeepAlive = millis();
    Serial.println("Sent KEEPALIVE to " + lastSenderIP.toString());
  }

  Serial.printf("packet size = %d\n", packetSize);
  Serial.println("[Server Connected] Check = " + String(check));
  Serial.println(WiFi.localIP());
}

void loop() {
  loopUDPServer();
}
