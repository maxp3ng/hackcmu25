import socket

UDP_IP = "127.0.0.1"   # local loopback
UDP_PORT = 4210
MESSAGE = "Hello from client"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

data, _ = sock.recvfrom(1024)
print("Server replied:", data.decode())

