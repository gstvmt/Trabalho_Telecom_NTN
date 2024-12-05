import cv2
import socket
import struct
import numpy as np
import time

MAX_DGRAM = 2**16
COUNT_LIMIT = 255

# Configurar o socket UDP
server_address = ("localhost", 5005)
client_address = ("localhost", 5080)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(client_address)

print(f"Client iniciado em {client_address[0]}:{client_address[1]}. Aguardando cliente...")

client.sendto("Estabelecendo conexao client -> server".encode("utf-8"), server_address)

start_time = time.perf_counter()

msg, address = client.recvfrom(1024)
end_time = time.perf_counter()
ping = (end_time - start_time)*1000

print(f"Ping: {ping:.3f} ms")

print(msg.decode('utf-8'))

buffer = b''
expected_sequence_number = 0
lost_packets_count = 0

while True:
    message, address = client.recvfrom(MAX_DGRAM)

    sequence_number = struct.unpack("BB", message[0:2])[0]
    if expected_sequence_number != sequence_number:
        print(f"Perda de pacote detectada. Esperado: {expected_sequence_number}, Recebido: {sequence_number}")
        lost_packets_count += 1

    expected_sequence_number = (expected_sequence_number + 1)%COUNT_LIMIT

    if struct.unpack("BB", message[0:2])[1] > 1:
        buffer += message[2:]
    else:
        buffer += message[2:]
        img = cv2.imdecode(np.fromstring(buffer, dtype=np.uint8), 1)
        cv2.imshow("frame", img)
        if cv2.waitKey(1) == 27:
            break
        buffer = b''


print(f"Ocorreram {lost_packets_count} perdas de pacote!")  

with open("dados.txt", "w") as arquivo:
    arquivo.write(f"Ping: {ping:.3f} ms\n")
    arquivo.write(f"Lost Packets: {lost_packets_count}")

cv2.destroyAllWindows()
client.close()
