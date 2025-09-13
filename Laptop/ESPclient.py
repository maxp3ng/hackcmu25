import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"   # Or your local broker IP
PORT = 8000
TOPIC_SUB = "esp32/test/data"
TOPIC_PUB = "esp32/test/cmd"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    print(f"Received from ESP32: {msg.payload.decode()}")

client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.publish(TOPIC_PUB, "LED_OFF")

client.loop_forever()

