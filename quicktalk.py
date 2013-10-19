import socket
UDP_IP = "127.0.0.1"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto("asdf", (UDP_IP, UDP_PORT))
