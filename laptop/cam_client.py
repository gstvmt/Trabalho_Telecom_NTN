import cv2
import socket
import struct
import numpy as np
import time
import os
from datetime import datetime

MAX_DGRAM = 2**16
COUNT_LIMIT = 255

buffer = b''
expected_sequence_number = 0
lost_packets_count = 0
total_data_received = 0
bandwidth_start_time = time.time()

# Variáveis para métricas
frame_start_time = time.time()
frames_received = 0
jitter_list = []
last_packet_time = time.time()
max_bandwidth = 21  # largura de banda máxima disponível  ??(CAPACIDADE DO CANAL) (em MB/s)
last_save_time = time.time()  # Controle de gravação de métricas
decode_times = [] # decodificação
latencies = [] # latência

# Configurar o socket UDP
server_address = ("localhost", 5005)
client_address = ("localhost", 5080)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(client_address)

print(f"Client iniciado em {client_address[0]}:{client_address[1]}. Aguardando cliente...")

client.sendto(struct.pack("d", time.time()), server_address)


while True:

    # Recebe mensagem
    message, address = client.recvfrom(MAX_DGRAM)
    total_data_received += len(message)

    """
    # Latência
    if len(message) == 8:  # Um pacote de timestamp terá exatamente 8 bytes
        # Processar o timestamp
        server_time = struct.unpack("d", message)[0]
        transmission_latency = time.time() - server_time
        latencies.append(transmission_latency)
        #Flooda a latencia no terminal
        #print(f"Latência: {transmission_latency:.4f} segundos")
        continue
    """

    header_size = struct.calcsize("BBd")

    # Analisar sequência Imagem
    sequence_number, segments_left, server_timestamp = struct.unpack("BBd", message[:header_size])

    if time.time() - server_timestamp > 0:
        latencies.append(time.time() - server_timestamp)
        print(time.time() - server_timestamp)

    if expected_sequence_number != sequence_number:
        #comentei a linha abaixo pra não ficar floodando o terminal
        #print(f"Perda de pacote detectada. Esperado: {expected_sequence_number}, Recebido: {sequence_number}")  
        lost_packets_count += 1

    expected_sequence_number = (expected_sequence_number + 1) % COUNT_LIMIT

    
    # Jitter
    current_time = time.time()
    jitter = abs(current_time - last_packet_time)
    jitter_list.append(jitter)
    last_packet_time = current_time
    

    # Buffer de imagem
    if struct.unpack("BBd", message[:header_size])[1] > 1:
        buffer += message[header_size:]
    else:
        buffer += message[header_size:]
        decode_start = time.time()
        img = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), 1)
        decode_time = time.time() - decode_start
        decode_times.append(decode_time)

        # Mostrar quadro

        try:
            cv2.imshow("frame", img)
            frames_received += 1
            buffer = b''
            if cv2.waitKey(1) == 27:
                break
        except Exception as e:
            print(f"Falha: {e}")
            buffer = b''
            continue


    

    # Largura de banda
    elapsed_time = time.time() - bandwidth_start_time
    if elapsed_time >= 5:  # Atualizar a cada 5 segundos
        bandwidth = (total_data_received / (1024 * 1024)) / elapsed_time  # MB/s
        utilization = (bandwidth / max_bandwidth) * 100
        print(f"Largura de Banda: {bandwidth:.2f} MB/s, Utilização da Rede: {utilization:.2f}%")
        total_data_received = 0
        bandwidth_start_time = time.time()

    # FPS Real
    if time.time() - frame_start_time >= 1:
        #print(f"FPS Recebidos: {frames_received}")
        frames_received = 0
        frame_start_time = time.time()

    """
    # Ping
    if expected_sequence_number == 0:
        client.sendto("ping".encode("utf-8"), server_address)
        ping_start_time = time.perf_counter()

        msg, address = client.recvfrom(1024)
        ping_end_time = time.perf_counter()
        ping = (ping_end_time - ping_start_time) * 1000  # Ping em ms

        ping_list.append(ping)

        print(f"Ping: {ping:.4f} ms")
    """

    # Salvar métricas no arquivo
    if time.time() - last_save_time >= 20:
        with open("metricas.txt", "a") as arquivo:  # "a" para anexar dados
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arquivo.write(f"\n[Dados registrados em: {current_time}]\n")
            arquivo.write(f"Jitter Médio: {np.mean(jitter_list):.3f} segundos\n")
            arquivo.write(f"Largura de Banda: {bandwidth:.2f} MB/s\n")
            arquivo.write(f"Utilização da Rede: {utilization:.2f}%\n")
            arquivo.write(f"Latência Média: {np.mean(latencies):.5f} segundos\n")
            arquivo.write(f"Tempo Médio de Decodificação: {np.mean(decode_times):.4f} segundos\n")
            arquivo.write(f"FPS Recebidos: {frames_received}\n")
        last_save_time = time.time()

    

print(f"Ocorreram {lost_packets_count} perdas de pacote!")  
file_path = os.path.join(os.getcwd(), "metricas.txt")
print(f"Salvando o arquivo de metricas em: {file_path}")

cv2.destroyAllWindows()
client.close()