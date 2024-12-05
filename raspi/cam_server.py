import cv2
import socket
import struct
import math
import time
import os

from utils.ruido_gaussiano import add_gaussian_noise

# Configurar o socket UDP
UDP_IP = "localhost"
UDP_PORT = 5005

MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64
CONT_LIMIT = 255

OUTPUT_DIR = "frames_server"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_IP, UDP_PORT))

print(f"Servidor iniciado em {UDP_IP}:{UDP_PORT}. Aguardando cliente...")

# Esperar pelo primeiro cliente
msg, address = server.recvfrom(1024)
server.sendto("Conexao estabelecida.".encode("utf-8"), address)

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
        
        frame_filename = os.path.join(OUTPUT_DIR, f"frame_{sequence_number}.jpg")
        cv2.imwrite(frame_filename, frame)
        
        # Simulacao de um ruido para test, tirar quando for fazer no drone
        frame_noisy = add_gaussian_noise(frame)

        _, buffer = cv2.imencode('.jpg', frame_noisy)
        # Alinha abaixo foi alterada por: DeprecationWarning: tostring() is deprecated. Use tobytes() instead. buffer = buffer.tostring()
        # buffer = buffer.tostring()
        buffer = buffer.tobytes()

        # Enviar o timestamp como pacote separado
        timestamp = time.time()
        timestamp_data = struct.pack("d", timestamp)
        server.sendto(timestamp_data, address)

        # Enviar a imagem segmentada
        size = len(buffer)
        num_of_segments = math.ceil(size / MAX_IMAGE_DGRAM)
        start = 0

        while num_of_segments:
            end = min(size, start + MAX_IMAGE_DGRAM)
            packet = struct.pack("BB", sequence_number, num_of_segments) + buffer[start:end]
            server.sendto(packet, address)
            start = end
            num_of_segments -= 1
            sequence_number = (sequence_number + 1) % CONT_LIMIT

finally:
    cap.release()
    server.close()
    print("Servidor encerrado")
