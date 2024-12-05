import cv2
import socket
import struct
import math

# Configurar o socket UDP
UDP_IP = "localhost"
UDP_PORT = 5005

MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_IP, UDP_PORT))

print(f"Servidor iniciado em {UDP_IP}:{UDP_PORT}. Aguardando cliente...")

# Esperar pelo primeiro cliente
msg, address = server.recvfrom(1024)
print(f"Cliente conectado: {address}")
print(msg.decode('utf-8'))

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera")
    server.close()
    exit()

sequence_number = 0

try:
    while True:

        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame")
            break

        _, buffer = cv2.imencode('.jpg', frame)
        buffer = buffer.tostring()
        size = len(buffer)
        num_of_segments = math.ceil(size/MAX_IMAGE_DGRAM)
        start = 0

        while num_of_segments:
            end = min(size, start + MAX_IMAGE_DGRAM)
            server.sendto(struct.pack("B", num_of_segments) + buffer[start : end], address)
            start = end
            num_of_segments -= 1

finally:
    cap.release()
    server.close()
    print("Servidor encerrado")