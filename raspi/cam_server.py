import cv2
import socket
import struct
import math
import time

# Configuração do servidor UDP
UDP_IP = "localhost"  # Endereço IP do servidor
UDP_PORT = 5005       # Porta utilizada pelo servidor

MAX_DGRAM = 2**16                   # Tamanho máximo de datagrama UDP
MAX_IMAGE_DGRAM = MAX_DGRAM - 64    # Tamanho máximo permitido para os pacotes de imagem
CONT_LIMIT = 255                    # Limite do contador de sequência (evita overflow)

# Inicialização do socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((UDP_IP, UDP_PORT))
print(f"Servidor iniciado em {UDP_IP}:{UDP_PORT}. Aguardando cliente...")

# Espera pela conexão do primeiro cliente
msg, address = server.recvfrom(1024)  # Recebe uma mensagem inicial do cliente
print(f"Cliente conectado: {address}")

# Sincronização de tempo entre cliente e servidor
client_time = struct.unpack("d", msg)[0]  # Tempo enviado pelo cliente
time_offset = client_time - time.time()   # Calcula a diferença entre os relógios do cliente e do servidor

# Configuração da captura de vídeo
cap = cv2.VideoCapture(0)  # Acessa a câmera (índice 0)

if not cap.isOpened():  # Verifica se a câmera foi aberta com sucesso
    print("Erro ao abrir a câmera")
    server.close()
    exit()

# Inicializa o número de sequência dos pacotes
sequence_number = 0

try:
    while True:
        # Captura um frame da câmera
        ret, frame = cap.read()
        if not ret:  # Verifica se a captura foi bem-sucedida
            print("Erro ao capturar frame")
            break

        # Codifica o frame em formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        buffer = buffer.tobytes()  # Converte para bytes

        # Obtém o tamanho do buffer e calcula o número de segmentos necessários
        size = len(buffer)
        num_of_segments = math.ceil(size / MAX_IMAGE_DGRAM)
        start = 0

        # Calcula o timestamp sincronizado com o relógio do cliente
        timestamp = time.time() + time_offset

        # Envia os segmentos da imagem
        while num_of_segments:
            end = min(size, start + MAX_IMAGE_DGRAM)  # Define o final do segmento atual
            # Cria o pacote com sequência, número de segmentos restantes e timestamp
            packet = struct.pack("BBd", sequence_number, num_of_segments, timestamp) + buffer[start:end]
            server.sendto(packet, address)  # Envia o pacote ao cliente
            start = end
            num_of_segments -= 1
            # Incrementa o número de sequência, reiniciando ao atingir o limite
            sequence_number = (sequence_number + 1) % CONT_LIMIT

finally:
    # Finaliza a captura de vídeo e o servidor
    cap.release()  # Libera a câmera
    server.close()  # Fecha o socket
    print("Servidor encerrado")
