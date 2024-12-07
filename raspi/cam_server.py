import cv2
import socket
import struct
import math
import time

# Configurar o socket UDP
UDP_IP = "localhost"
UDP_PORT = 5005

MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64
CONT_LIMIT = 255

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_IP, UDP_PORT))

print(f"Servidor iniciado em {UDP_IP}:{UDP_PORT}. Aguardando cliente...")

# Esperar pelo primeiro cliente
msg, address = server.recvfrom(1024)
print(f"Cliente conectado: {address}")

client_time = struct.unpack("d", msg)[0]    # Armazena o tempo do relógio do client
time_offset = client_time - time.time()     # Calcula a diferença de tempo entre os dois relógios

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
        # Alinha abaixo foi alterada por: DeprecationWarning: tostring() is deprecated. Use tobytes() instead. buffer = buffer.tostring()
        # buffer = buffer.tostring()
        buffer = buffer.tobytes()

        """
        # Enviar o timestamp como pacote separado
        timestamp = time.time()
        timestamp_data = struct.pack("d", timestamp)
        server.sendto(timestamp_data, address)
        """

        # Enviar a imagem segmentada
        size = len(buffer)
        num_of_segments = math.ceil(size / MAX_IMAGE_DGRAM)
        start = 0

        timestamp = time.time() + time_offset

        while num_of_segments:
            end = min(size, start + MAX_IMAGE_DGRAM)
            packet = struct.pack("BBd", sequence_number, num_of_segments, timestamp) + buffer[start:end]
            server.sendto(packet, address)
            start = end
            num_of_segments -= 1
            sequence_number = (sequence_number + 1) % CONT_LIMIT
        
        """
        # A cada 256 sequencias, calcula o ping
        if sequence_number == 0:
            time_test_start = time.perf_counter()
            msg, address = server.recvfrom(1024)
            server.sendto("pong".encode("utf-8"), address)
            time_test_end = time.perf_counter()
            tempo_teste = (time_test_end - time_test_end)*1000
            print(f"{tempo_teste:.5f}\n")
        """


finally:
    cap.release()
    server.close()
    print("Servidor encerrado")