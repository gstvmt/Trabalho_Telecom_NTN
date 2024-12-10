import cv2
import socket
import struct
import numpy as np
import time
import os
from datetime import datetime

MAX_DGRAM = 2**16           # Tamanho máximo de datagrama UDP
COUNT_LIMIT = 255           # Limite do contador da sequência

# Variáveis para controle
buffer = b''                        # Buffer de reconstrução da imagem
expected_sequence_number = 0        # Número da sequência esperado, enviado pelo servidor
bandwidth_start_time = time.time()  # Tempo inicial para cálculo da largura de banda
last_packet_time = time.time()      # Tempo do último pacote recebido
max_bandwidth = 21                  # largura de banda máxima disponível
last_save_time = time.time()        # Controle de gravação de métricas
frame_start_time = time.time()      # Tempo inicial para cálculo de fps

# Variáveis para métricas
total_data_received = 0             # Quantidade de bytes recebidos no total
lost_packets_count = 0              # Quantidade de perdas de pacote
frames_received = 0                 # Quantidade de quadros recebidos
jitter_list = []                    # Lista dos valores de jutter coletados
latencies = []                      # Lista dos valores de latência coletados
decode_times = []                   # Lista dos tempos de codifição coletados

# Configurar o socket UDP
server_address = ("localhost", 5005)        # Endereço do servidor
client_address = ("localhost", 5080)        # Enderedo do client

# Incialização do socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(client_address)

print(f"Client iniciado em {client_address[0]}:{client_address[1]}. Aguardando cliente...")

client.sendto(struct.pack("d", time.time()), server_address)        # Avisa a conexão para o servidor e envia o tempo para sincronização


while True:

    # Recebe a mensagem do servidor
    message, address = client.recvfrom(MAX_DGRAM)
    total_data_received += len(message)             # Define o tamanho da mensagem recebida

    header_size = struct.calcsize("BBd")            # Tamanho do cabeçalho do pacote (sequência, segmentos restates, timestamp)
    sequence_number, segments_left, server_timestamp = struct.unpack("BBd", message[:header_size])      # Desempacota a mensagem e salva cada parte nas respectivas variáveis

    # Calcula a latência e salva na lista
    if time.time() - server_timestamp > 0:
        latencies.append(time.time() - server_timestamp)
        #print(time.time() - server_timestamp)

    # Verifica se a sequência que o client tem é a mesma do servidor. Se não for, houve perda de pacote, então isso é registrado.
    if expected_sequence_number != sequence_number:
        #print(f"Perda de pacote detectada. Esperado: {expected_sequence_number}, Recebido: {sequence_number}")  
        lost_packets_count += 1

    expected_sequence_number = (expected_sequence_number + 1) % COUNT_LIMIT     # Redefine a sequência do client para ser a mesma do servidor, para corrigir no caso de dessincronia

    
    # Calcula o jitter e salva na lista
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
        img = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), 1)        # Decodifica a imagem
        
        # Calcula o tempo de decodificação e armazena o resultado
        decode_time = time.time() - decode_start
        decode_times.append(decode_time)

        # Mostra o quadro decodificado
        try:
            cv2.imshow("frame", img)    # Mostra a imagem
            frames_received += 1        # Aumenta o número de frames recebidos
            buffer = b''                # Limpa o buffer
            if cv2.waitKey(1) == 27:    # Caso a tecla esc for pressionada fecha o programa
                break
        except Exception as e:          # No caso de algum erro com a exibição da image, imprime a falha, limpa o buffer e continua
            print(f"Falha: {e}")
            buffer = b''
            continue


    

    # Calcula a largura de banda usada na rede
    elapsed_time = time.time() - bandwidth_start_time
    if elapsed_time >= 5:  # Atualizar a cada 5 segundos
        bandwidth = (total_data_received / (1024 * 1024)) / elapsed_time  # MB/s
        utilization = (bandwidth / max_bandwidth) * 100
        print(f"Largura de Banda: {bandwidth:.2f} MB/s, Utilização da Rede: {utilization:.2f}%")
        total_data_received = 0
        bandwidth_start_time = time.time()

    # FPS Real
    if time.time() - frame_start_time >= 1:         # Ocorre a cada segundo
        #print(f"FPS Recebidos: {frames_received}")
        frames_received = 0
        frame_start_time = time.time()

    # Anexa as métricas no arquivo
    if time.time() - last_save_time >= 10:      # Ocorre a cada 10 segundos
        with open("metricas.txt", "a") as arquivo:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arquivo.write(f"\n[Dados registrados em: {current_time}]\n")
            arquivo.write(f"Jitter Médio: {np.mean(jitter_list):.3f} segundos\n")
            arquivo.write(f"Largura de Banda: {bandwidth:.2f} MB/s\n")
            arquivo.write(f"Utilização da Rede: {utilization:.2f}%\n")
            arquivo.write(f"Latência Média: {np.mean(latencies):.5f} segundos\n")
            arquivo.write(f"Tempo Médio de Decodificação: {np.mean(decode_times):.4f} segundos\n")
            arquivo.write(f"FPS Recebidos: {frames_received}\n")
        last_save_time = time.time()

    
# Finalização do client
print(f"Ocorreram {lost_packets_count} perdas de pacote!")  
file_path = os.path.join(os.getcwd(), "metricas.txt")
print(f"Salvando o arquivo de metricas em: {file_path}")

cv2.destroyAllWindows()
client.close()