import cv2
import socket
import struct
import numpy as np

MAX_DGRAM = 2**16

# Configurar o socket UDP
server_adress = ("localhost", 5005)
client_adress = ("localhost", 5080)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(client_adress)

print(f"Client iniciado em {client_adress[0]}:{client_adress[1]}. Aguardando cliente...")

client.sendto("Estabelecendo conexao client -> server".encode("utf-8"), server_adress)

buffer = b''
expected_sequence_number = 0
lost_packets_count = 0

while True:
    message, adress = client.recvfrom(MAX_DGRAM)

    if struct.unpack("B", message[0:1])[0] > 1:
        buffer += message[1:]
    else:
        buffer += message[1:]
        img = cv2.imdecode(np.fromstring(buffer, dtype=np.uint8), 1)
        cv2.imshow("frame", img)
        if cv2.waitKey(1) == 27:
            break
        buffer = b''

   
cv2.destroyAllWindows()
client.close()
