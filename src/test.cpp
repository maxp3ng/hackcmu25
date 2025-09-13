#include <Arduino.h>

// Built-in LED pin for ESP32-S3 DevKit-C
#define LED_PIN 48

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
  // Wait for serial connection (optional, remove if not using serial monitor)
  delay(1000);
  
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println();
  Serial.println("ESP32-S3 Black Triangle Test");
  Serial.println("=============================");
  Serial.print("ESP32 Chip model: ");
  Serial.println(ESP.getChipModel());
  Serial.print("ESP32 Chip revision: ");
  Serial.println(ESP.getChipRevision());
  Serial.print("Flash size: ");
  Serial.print(ESP.getFlashChipSize() / (1024 * 1024));
  Serial.println(" MB");
  Serial.print("PSRAM size: ");
  Serial.print(ESP.getPsramSize() / (1024 * 1024));
  Serial.println(" MB");
  Serial.print("Free heap: ");
  Serial.print(ESP.getFreeHeap() / 1024);
  Serial.println(" KB");
  Serial.println();
  Serial.println("LED blinking started - your ESP32-S3 is working!");
  Serial.println("=============================");
}

void loop() {
  // Blink the LED
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ON");
  delay(1000);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED OFF");
  delay(1000);
}

