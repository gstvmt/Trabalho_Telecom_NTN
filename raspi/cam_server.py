# Código na Raspberry Pi (Servidor)
# Pega as informaçoes da camera e as envia para o computador
import time
import pickle
import socket
import cv2

# Configuração do servidor
HOST = '0.0.0.0'
PORT = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Aguardando conexão...")

conn, addr = server_socket.accept()
print(f"Conectado a {addr}")

# Configuração da câmera
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break
    timestamp = time.time()  # Marca o horário do envio
    data = pickle.dumps((timestamp, frame))  # Envia timestamp junto com a imagem
    conn.sendall(data)

camera.release()
conn.close()
server_socket.close()
