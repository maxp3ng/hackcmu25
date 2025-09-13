#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
WiFiUDP udp;
char packetBuffer[255];
unsigned int localPort = 9999;
const char *ssid = "ESP_EcoDrive";
const char *password = "alex";

// Pin definitions
int redPin = 17;
int greenPin = 16;
int bluePin = 15;

// Channels for ESP32 PWM (each pin needs its own channel)
int redChannel = 0;
int greenChannel = 1;
int blueChannel = 2;

// Frequency and resolution
int freq = 5000;          // 5 kHz PWM
int resolution = 8;       // 8-bit (0–255)

#define PORT 8080 


void setColor(int redValue, int greenValue, int blueValue) {
  ledcWrite(redChannel, 255 - redValue);
  ledcWrite(greenChannel, 255 - greenValue);
  ledcWrite(blueChannel, 255 - blueValue);
}

void setupWifi(){
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED){
    delay(500); Serial.print(F("."));
  }
  //init
  udp.begin(localPort);
  Serial.printf("UDP server : %s:%i \n", WiFi.localIP().toString().c_str(), localPort);
}

void setup() {
  // Attach pins to PWM channels
  ledcSetup(redChannel, freq, resolution);
  ledcAttachPin(redPin, redChannel);

  ledcSetup(greenChannel, freq, resolution);
  ledcAttachPin(greenPin, greenChannel);

  ledcSetup(blueChannel, freq, resolution);
  ledcAttachPin(bluePin, blueChannel);
  setupWifi();
}

void loopUDPServer(){
  int packetSize = udp.parsePacket();
  Serial.print("receive from :"); Serial.println(udp.remoteIP());
  Serial.print("size : "); Serial.println(packetSize);
  if (packetSize) {
    int len = udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len - 1] = 0;
    Serial.printf("Data : %s\n", packetBuffer);
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.printf("UDP packet was received OK\r\n");
    udp.endPacket();
  }
  Serial.println("\n");
  delay(500);
  Serial.print("[Server Connected] ");
  Serial.println (WiFi.localIP());
}

void loop() {
  Serial.begin(115200);
  Serial.println("[Server running] ");
  loopUDPServer();
  setColor(255, 0, 0);   // Red
}