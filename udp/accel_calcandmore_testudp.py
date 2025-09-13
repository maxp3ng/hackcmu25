import math as Math
import socket
import json

# UDP setup
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 0 #5005     # Change to your port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

accel_thresh1 = [0, 0.075, 0.075*2, 0.075*3, 0.3, 0.45]
accel_thresh2 = [0, 0.0345, 0.0688, 0.1033, 0.1378, 0.206]
decel_thresh = [0, 0.051, 0.102, 0.153, 0.204, 0.256]

thresh_type = 1

print("Listening for UDP data...")

skip_first = True

while True:
    data_bytes, addr = sock.recvfrom(4096)
    data_str = data_bytes.decode('utf-8')

    # Skip if the first message contains "Listening on UDP 4210..."
    if skip_first and "Listening on UDP 4210..." in data_str:
        skip_first = False
        continue

    try:
        data = json.loads(data_str)
    except Exception as e:
        print(f"Error decoding data: {e}")
        continue

    accelX = data["accelX"]
    accelY = data["accelY"]
    accelZ = data["accelZ"]
    gyroX = data["gyroX"]
    gyroY = data["gyroY"]
    gyroZ = data["gyroZ"] + 1
    gyroTime = data["gyroTime"]

    dot = accelX*gyroX + accelY*gyroY + accelZ*gyroZ
    accel_magnitude = Math.sqrt(accelX*accelX + accelY*accelY + accelZ*accelZ)

    led_pos = 3  # Reset for each packet

    if dot >= 0:   # accelerating
        if thresh_type == 1:
            while led_pos <= 5 and accel_magnitude > accel_thresh1[led_pos]:
                led_pos += 1
            if led_pos < 3:
                thresh_type = 2
        if thresh_type == 2:
            while led_pos <= 5 and accel_magnitude > accel_thresh2[led_pos]:
                led_pos += 1
            if accel_magnitude > accel_thresh1[4]:
                thresh_type = 1
    else:   # decelerating
        while led_pos <= 5 and accel_magnitude > decel_thresh[led_pos]:
            led_pos += 1

    if led_pos > 6:
        led_pos = 6

    print(f"dot: {dot}, accel magnitude: {accel_magnitude}")
    print(f"accelerating: {dot > 0}, thresh_type: {thresh_type}, led_pos: {led_pos}")
