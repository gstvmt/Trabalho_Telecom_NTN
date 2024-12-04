# Código no Computador (Cliente)
# recebe as imagens por meio da rede wifi e avalia o meio de comunicaçao.

import socket
import pickle
import time
import cv2

# Configuração do cliente
HOST = '192.168.1.X'  # IP da Raspberry Pi
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

received_packets = 0
missed_packets = 0

while True:
    data = client_socket.recv(4096)
    if not data:
        break
    try:
        timestamp, frame = pickle.loads(data)
        # Verifica se o timestamp está dentro do esperado
        if timestamp:
            received_packets += 1
        else:
            missed_packets += 1
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        missed_packets += 1

client_socket.close()
cv2.destroyAllWindows()

# Relatório da perda de pacotes
print(f"Pacotes recebidos: {received_packets}")
print(f"Pacotes perdidos: {missed_packets}")
