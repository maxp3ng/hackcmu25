import math as Math
import socket
import json
from collections import deque
import matplotlib.pyplot as plt
import signal
import sys

# UDP setup
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

accel_thresh1 = [0, 0.075, 0.075*2, 0.075*3, 0.3, 0.45]
accel_thresh2 = [0, 0.0345, 0.0688, 0.1033, 0.1378, 0.206]
decel_thresh = [0, 0.051, 0.102, 0.153, 0.204, 0.256]

thresh_type = 1
t_ledpos = 0
t_samples = 0

d_score = 0
d_analysis_score = []
d_analysis_time = []


print("Listening for UDP data...")

skip_first = True

# Moving average window size
WINDOW_SIZE = 15
accelX_window = deque(maxlen=WINDOW_SIZE)
accelY_window = deque(maxlen=WINDOW_SIZE)
accelZ_window = deque(maxlen=WINDOW_SIZE)

# Rolling average window for LED output smoothing
LED_WINDOW_SIZE = 5
led_output_window = deque(maxlen=LED_WINDOW_SIZE)

LED_POS_WINDOW_SIZE = 5
led_pos_window = deque(maxlen=LED_POS_WINDOW_SIZE)

prev_time = None
prev_accelX_avg = None
prev_accelY_avg = None
prev_accelZ_avg = None

def plot_and_exit(signum, frame):
    print("\nTerminating and plotting score graph...")
    if len(d_analysis_time) > 0 and len(d_analysis_score) > 0:
        plt.figure(figsize=(10, 6))
        plt.plot(d_analysis_time, d_analysis_score, marker='o')
        plt.xlabel("Time (ms)")
        plt.ylabel("Score (avg per 10 samples)")
        plt.title("Score vs Time")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("score_vs_time.png")
        plt.show()
    else:
        print("No data to plot.")
    sys.exit(0)

signal.signal(signal.SIGINT, plot_and_exit)

while True:
    data_bytes, addr = sock.recvfrom(4096)
    data_str = data_bytes.decode('utf-8')

    if skip_first and "Listening on UDP 4210..." in data_str:
        skip_first = False
        continue

    try:
        data = json.loads(data_str)
    except Exception as e:
        print(f"Error decoding data: {e}")
        continue

    gravityX = data["gravityX"]
    gravityY = data["gravityY"]
    gravityZ = data["gravityZ"]

    accelX = data["accelX"] - gravityX
    accelY = data["accelY"] - gravityY
    accelZ = data["accelZ"] - gravityZ
    accelTime = data["accelTime"]

    gyroX = data["gyroX"]
    gyroY = data["gyroY"]
    gyroZ = data["gyroZ"]
    gyroTime = data["gyroTime"]

    # Add to moving average window
    accelX_window.append(accelX)
    accelY_window.append(accelY)
    accelZ_window.append(accelZ)

    # Calculate moving average
    accelX_avg = sum(accelX_window) / len(accelX_window)
    accelY_avg = sum(accelY_window) / len(accelY_window)
    accelZ_avg = sum(accelZ_window) / len(accelZ_window)

    # Calculate jerk (derivative of smoothed acceleration)
    jerkX = jerkY = jerkZ = jerkT = 0.0
    if prev_time is not None:
        dt = (accelTime - prev_time) / 1000.0  # convert ms to seconds if needed
        if dt > 0:
            jerkX = (accelX_avg - prev_accelX_avg) / dt
            jerkY = (accelY_avg - prev_accelY_avg) / dt
            jerkZ = (accelZ_avg - prev_accelZ_avg) / dt
            jerkT = Math.sqrt(jerkX*jerkX + jerkY*jerkY + jerkZ*jerkZ)

    prev_time = accelTime
    prev_accelX_avg = accelX_avg
    prev_accelY_avg = accelY_avg
    prev_accelZ_avg = accelZ_avg

    dot = accelX*gyroX + accelY*gyroY + accelZ*gyroZ
    accel_magnitude = Math.sqrt(accelX*accelX + accelY*accelY + accelZ*accelZ)

    led_pos = 0  # Reset for each packet

    if dot >= 0:   # accelerating
        if jerkT > 450:
            thresh_type = 1
        else:
            thresh_type = 2
        

        if thresh_type == 1:
            while led_pos <= 5 and accel_magnitude > accel_thresh1[led_pos]:
                led_pos += 1
        if thresh_type == 2:
            while led_pos <= 5 and accel_magnitude > accel_thresh2[led_pos]:
                led_pos += 1
    else:   # decelerating
        while led_pos <= 5 and accel_magnitude > decel_thresh[led_pos]:
            led_pos += 1

    if led_pos > 6:
        led_pos = 6
    if led_pos < 0:
        led_pos = 0

    led_pos_window.append(led_pos)
    smoothed_led_pos = int(round(sum(led_pos_window) / len(led_pos_window)))

    if smoothed_led_pos > 6:
        smoothed_led_pos = 6
    if smoothed_led_pos < 0:
        smoothed_led_pos = 0

    LED_postable = [100,80,60,40,20,0]
    if thresh_type == 1 and dot > 0:
        LED_postable = [100,90,80,70,65,60]

    led_output = LED_postable[smoothed_led_pos - 1] if smoothed_led_pos > 0 else 0

    t_ledpos += led_output
    t_samples += 1

    if (t_samples % 10) == 0:
        # take average of the past 10 samples
        d_analysis_score.append(d_score / 10)
        d_analysis_time.append(accelTime)
        d_score = 0

    score = t_ledpos / t_samples if t_samples > 0 else 0
    score = (19/16) * score
    if score > 100:
        score = 100
    if score < 0:
        score = 0
    score = int(score)
    d_score += score

    print(f"led_pos: {smoothed_led_pos}, thresh_type: {thresh_type}, score: {score}")



