import cv2
import socket
import struct
import math
import time

# Configurar o socket UDP
UDP_IP = "localhost"                # Endereço IP do servidor
UDP_PORT = 5005                     # Porta do servidor

MAX_DGRAM = 2**16                   # Tamanho máximo de datagrama UDP
MAX_IMAGE_DGRAM = MAX_DGRAM - 64    # Tamanho máximo para os pacotes de imagem
CONT_LIMIT = 255                    # Limite do contador da sequência

# Inicialização do socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_IP, UDP_PORT))

print(f"Servidor iniciado em {UDP_IP}:{UDP_PORT}. Aguardando cliente...")

# Esperar pelo primeiro cliente
<<<<<<< Updated upstream
msg, address = server.recvfrom(1024)
server.sendto("Conexao estabelecida.".encode("utf-8"), address)
print(f"Cliente conectado: {address}")
print(msg.decode("utf-8"))
=======
msg, address = server.recvfrom(1024)        # Recebe uma mensagem inicial do client (que é o tempo atual do client), indicando a conexão
print(f"Cliente conectado: {address}")

# Sincronização de tempo entre client e servidor
client_time = struct.unpack("d", msg)[0]    # Armazena o tempo do relógio do client
time_offset = client_time - time.time()     # Calcula a diferença de tempo entre os dois relógios
>>>>>>> Stashed changes

cap = cv2.VideoCapture(0)                   # Acessa a câmera de índice 0

# Verifica se a câmera foi aberta com sucesso
if not cap.isOpened():
    print("Erro ao abrir a câmera")
    server.close()
    exit()

sequence_number = 0        # Inicialização da sequência dos pacotes

try:
    while True:
        ret, frame = cap.read()        # Captura 1 frame da câmera
        if not ret:                    # Verifica se a captura foi bem sucedida
            print("Erro ao capturar frame")
            break

        # Codifica o frame no formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        buffer = buffer.tobytes()

<<<<<<< Updated upstream
        # Enviar o timestamp como pacote separado
        timestamp = time.time()
        timestamp_data = struct.pack("d", timestamp)
        server.sendto(timestamp_data, address)

        # Enviar a imagem segmentada
=======
        # Segmenta a imagem de acordo com o tamanho do buffer
>>>>>>> Stashed changes
        size = len(buffer)
        num_of_segments = math.ceil(size / MAX_IMAGE_DGRAM)
        start = 0

<<<<<<< Updated upstream
        while num_of_segments:
            end = min(size, start + MAX_IMAGE_DGRAM)
            packet = struct.pack("BB", sequence_number, num_of_segments) + buffer[start:end]
=======
        timestamp = time.time() + time_offset        # Calcula o timestamp sincronizado com o relógio do client

        # Envia os segmentos da imagem
        while num_of_segments:
            end = min(size, start + MAX_IMAGE_DGRAM)        # Define o segmento atual
            # Cria o pacote com a sequência, número de segmentos restantes e o timestamp e envia para o client
            packet = struct.pack("BBd", sequence_number, num_of_segments, timestamp) + buffer[start:end]
>>>>>>> Stashed changes
            server.sendto(packet, address)
            start = end
            num_of_segments -= 1
            sequence_number = (sequence_number + 1) % CONT_LIMIT
<<<<<<< Updated upstream
        
        # A cada 256 sequencias, calcula o ping
        if sequence_number == 0:
            time_test_start = time.perf_counter()
            msg, address = server.recvfrom(1024)
            server.sendto("pong".encode("utf-8"), address)
            time_test_end = time.perf_counter()
            tempo_teste = (time_test_end - time_test_end)*1000
            print(f"{tempo_teste:.5f}\n")

=======
>>>>>>> Stashed changes

finally:
    # Finaliza a captura de vídeo liberando a câmera, e fecha o servidor.
    cap.release()
    server.close()
    print("Servidor encerrado")