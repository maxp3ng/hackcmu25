#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>


unsigned int localPort = 8000;
const char *ssid = "shado";
const char *password = "poopypoo";
const char* broker = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.print("Message arrived: ");
  Serial.println(msg);

  //alex edit these 
  if (msg == "LED_0") digitalWrite(2, HIGH);
  if (msg == "LED_1") digitalWrite(2, HIGH);
  if (msg == "LED_2") digitalWrite(2, HIGH);
  if (msg == "LED_3") digitalWrite(2, HIGH);
  if (msg == "LED_4") digitalWrite(2, HIGH);
  if (msg == "LED_5") digitalWrite(2, HIGH);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      client.subscribe("esp32/test/cmd");
    } else {
      delay(5000);
    }
  }
}

void setupWifi(){
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED){
    delay(500); Serial.print(F("."));
  }
  //init
  client.setServer(broker, 1883);
  client.setCallback(callback);
}

void setup() {
  pinMode(2, OUTPUT);
  Serial.begin(115200);
  setupWifi();
 }

void loopMQTTServer(){
  delay(500);
  Serial.print("[Server Connected] ");
  Serial.println (WiFi.localIP());
}

void loop() {
  Serial.println("[Server running] ");
  loopMQTTServer();
}
