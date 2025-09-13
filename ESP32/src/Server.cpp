#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>


unsigned int localPort = 1883;
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

  if (msg == "LED_ON") digitalWrite(2, HIGH);
  if (msg == "LED_OFF") digitalWrite(2, LOW);
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
  client.setServer(broker, localPort);
  client.setCallback(callback);
}

void setup() {
  Serial.begin(115200);
  delay(500);
  pinMode(2, OUTPUT);
  setupWifi();
 }

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  Serial.println("[Server running] ");
  delay(500);
  Serial.println (WiFi.localIP());
}
