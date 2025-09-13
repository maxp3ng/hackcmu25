import math as Math
import time

milliseconds1 = int(time.time() * 1000)


data = {"rot11":-0.6586852073669434,"accelZ":-0.8597259521484375,"gravityZ":-0.9882218837738037,"magZ":-110.80632019042969,"gyroTime":62301.64968966667,"rot12":-0.739879310131073,"quatX":-0.07666075704963593,"quatW":0.40593168723193623,"gyroX":0.2884184718132019,"accelTime":62301.64213866667,"roll":-7.88102072266364,"gyroY":-0.1247406005859375,"rot33":0.9882218837738037,"magY":42.242767333984375,"latitude":40.44160222662698,"magX":-55.01924133300781,"rot31":0.14245890080928802,"motionTime":62301.64843166667,"rot13":0.13679347932338715,"quatY":0.003489148903321062,"accelY":0.2409515380859375,"magTime":62301.61936366667,"rot22":-0.6704146265983582,"seq":32505,"pitch":-3.9331794024672386,"yaw":-132.22140969356764,"gravityY":0.06859302520751953,"longitude":-79.93882659870242,"rot32":0.05588309466838837,"accelX":-0.0602874755859375,"rot21":0.7388094067573547,"gravityX":-0.13679347932338715,"gyroZ":-0.17445729672908783,"rot23":-0.06859303265810013,"quatZ":-0.910675827233177}

accelX = data["accelX"]
accelY = data["accelY"]
accelZ = data["accelZ"]
gyroX = data["gyroX"]
gyroY = data["gyroY"]
gyroZ = data["gyroZ"] + 1 
gyroTime = data["gyroTime"]

dot = accelX*gyroX + accelY*gyroY + accelZ*gyroZ
accel_magnitude = Math.sqrt(accelX*accelX + accelY*accelY + accelZ*accelZ)

print(f"dot: {dot}, accel magnitude: {accel_magnitude}")

accel_thresh1 = [0,0.075,0.075*2,0.075*3,0.3, 0.45]
accel_thresh2 = [0,0.0345,0.0688,0.1033,0.1378,0.206]
decel_thresh = [0,0.051,0.102,0.153,0.204,0.256]
thresh_type = 1
led_pos = 3

if (dot >= 0):   # accelerating
    if (thresh_type == 1):
        while (led_pos < 5 and accel_magnitude > accel_thresh1[led_pos]):
            led_pos += 1
        if (led_pos < 3):
            thresh_type = 2
    if (thresh_type == 2):
        while (led_pos < 5 and accel_magnitude > accel_thresh2[led_pos]):
            led_pos += 1
        if (accel_magnitude > accel_thresh1[4]):
            thresh_type = 1
else:   # decelerating
    while (led_pos < 5 and accel_magnitude > decel_thresh[led_pos]):
        led_pos += 1

print(f"accelerating: {dot > 0}, thresh_type: {thresh_type}, led_pos: {led_pos + 1}")

milliseconds2 = int(time.time() * 1000)
print(f"Time taken: {milliseconds2 - milliseconds1} ms")

'''
// find out if i am acceelrating (dot product of accel and gyro vectors)
// threshold is 0.5 m/s^2
// once up to speed (when ), threshold is 0.2 m/s^2

//if decellerating (negative dot product) then threshold is 0.5 m/s^2

'''



