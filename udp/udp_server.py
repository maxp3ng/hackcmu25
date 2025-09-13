import socket

UDP_IP = "0.0.0.0"   # listen on all interfaces
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on UDP {UDP_PORT}...")
while True:
    data, addr = sock.recvfrom(1024)
    print(data.decode())
    print(addr)
    sock.sendto(b"Echo: " + data, addr)
