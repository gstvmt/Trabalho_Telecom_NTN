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
<<<<<<< Updated upstream
frame_start_time = time.time()
frames_received = 0
jitter_list = []
last_packet_time = time.time()
max_bandwidth = 21  # largura de banda máxima disponível  ??(CAPACIDADE DO CANAL) (em MB/s)
last_save_time = time.time()  # Controle de gravação de métricas
decode_times = [] # decodificação
latencies = [] # latência
ping_list = []
=======
total_data_received = 0             # Quantidade de bytes recebidos no total
lost_packets_count = 0              # Quantidade de perdas de pacote
frames_received = 0                 # Quantidade de quadros recebidos
jitter_list = []                    # Lista dos valores de jutter coletados
latencies = []                      # Lista dos valores de latência coletados
decode_times = []                   # Lista dos tempos de codifição coletados
>>>>>>> Stashed changes

# Configurar o socket UDP
server_address = ("localhost", 5005)        # Endereço do servidor
client_address = ("localhost", 5080)        # Enderedo do client

# Incialização do socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(client_address)

print(f"Client iniciado em {client_address[0]}:{client_address[1]}. Aguardando cliente...")

<<<<<<< Updated upstream
client.sendto("Estabelecendo conexao client -> server".encode("utf-8"), server_address)
=======
client.sendto(struct.pack("d", time.time()), server_address)        # Avisa a conexão para o servidor e envia o tempo para sincronização
>>>>>>> Stashed changes

# Calcula o Ping ao iniciar a conexão
ping_start_time = time.perf_counter()
msg, address = client.recvfrom(1024)
ping_end_time = time.perf_counter()
ping = (ping_end_time - ping_start_time) * 1000  # Ping em ms
ping_list.append(ping)

print(f"Ping: {ping:.3f} ms")
print(msg.decode('utf-8'))

while True:

    # Recebe a mensagem do servidor
    message, address = client.recvfrom(MAX_DGRAM)
    total_data_received += len(message)             # Define o tamanho da mensagem recebida

<<<<<<< Updated upstream
    # Latência
    if len(message) == 8:  # Um pacote de timestamp terá exatamente 8 bytes
        # Processar o timestamp
        server_time = struct.unpack("d", message)[0]
        transmission_latency = time.time() - server_time
        latencies.append(transmission_latency)
        #Flooda a latencia no terminal
        #print(f"Latência: {transmission_latency:.4f} segundos")
        continue

    # Analisar sequência Imagem
    sequence_number, segments_left = struct.unpack("BB", message[0:2])
    if expected_sequence_number != sequence_number:
        #comentei a linha abaixo pra não ficar floodando o terminal
       #print(f"Perda de pacote detectada. Esperado: {expected_sequence_number}, Recebido: {sequence_number}")  
=======
    header_size = struct.calcsize("BBd")            # Tamanho do cabeçalho do pacote (sequência, segmentos restates, timestamp)
    sequence_number, segments_left, server_timestamp = struct.unpack("BBd", message[:header_size])      # Desempacota a mensagem e salva cada parte nas respectivas variáveis

    # Calcula a latência e salva na lista
    if time.time() - server_timestamp > 0:
        latencies.append(time.time() - server_timestamp)
        #print(time.time() - server_timestamp)

    # Verifica se a sequência que o client tem é a mesma do servidor. Se não for, houve perda de pacote, então isso é registrado.
    if expected_sequence_number != sequence_number:
        #print(f"Perda de pacote detectada. Esperado: {expected_sequence_number}, Recebido: {sequence_number}")  
>>>>>>> Stashed changes
        lost_packets_count += 1

    expected_sequence_number = (expected_sequence_number + 1) % COUNT_LIMIT     # Redefine a sequência do client para ser a mesma do servidor, para corrigir no caso de dessincronia

<<<<<<< Updated upstream
    # Jitter
=======
    
    # Calcula o jitter e salva na lista
>>>>>>> Stashed changes
    current_time = time.time()
    jitter = abs(current_time - last_packet_time)
    jitter_list.append(jitter)
    last_packet_time = current_time

    # Buffer de imagem
    if struct.unpack("BB", message[0:2])[1] > 1:
        buffer += message[2:]
    else:
        buffer += message[2:]
        decode_start = time.time()
<<<<<<< Updated upstream
        # Alinha abaixo foi alterada por: DeprecationWarning: The binary mode of fromstring is deprecated, as it behaves surprisingly on unicode inputs. Use frombuffer instead
        # img = cv2.imdecode(np.fromstring(buffer, dtype=np.uint8), 1)
        img = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), 1)
        decode_time = time.time() - decode_start
        decode_times.append(decode_time)

        # Mostrar quadro
        cv2.imshow("frame", img)
        frames_received += 1
        buffer = b''
        if cv2.waitKey(1) == 27:
            break
=======
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


    
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    # Ping
    if expected_sequence_number == 0:
        client.sendto("ping".encode("utf-8"), server_address)
        ping_start_time = time.perf_counter()

        msg, address = client.recvfrom(1024)
        ping_end_time = time.perf_counter()
        ping = (ping_end_time - ping_start_time) * 1000  # Ping em ms

        ping_list.append(ping)

        print(f"Ping: {ping:.4f} ms")

    # Salvar métricas no arquivo
    if time.time() - last_save_time >= 20:
        with open("metricas.txt", "a") as arquivo:  # "a" para anexar dados
=======
    # Anexa as métricas no arquivo
    if time.time() - last_save_time >= 10:      # Ocorre a cada 10 segundos
        with open("metricas.txt", "a") as arquivo:
>>>>>>> Stashed changes
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            arquivo.write(f"\n[Dados registrados em: {current_time}]\n")
            arquivo.write(f"Ping Médio: {np.mean(ping_list):.3f} ms\n")
            arquivo.write(f"Jitter Médio: {np.mean(jitter_list):.3f} segundos\n")
            arquivo.write(f"Largura de Banda: {bandwidth:.2f} MB/s\n")
            arquivo.write(f"Utilização da Rede: {utilization:.2f}%\n")
            arquivo.write(f"Latência Média: {np.mean(latencies):.5f} segundos\n")
            arquivo.write(f"Tempo Médio de Decodificação: {np.mean(decode_times):.4f} segundos\n")
            arquivo.write(f"FPS Recebidos: {frames_received}\n")
        last_save_time = time.time()

<<<<<<< Updated upstream
=======
    
# Finalização do client
>>>>>>> Stashed changes
print(f"Ocorreram {lost_packets_count} perdas de pacote!")  
file_path = os.path.join(os.getcwd(), "metricas.txt")
print(f"Salvando o arquivo de metricas em: {file_path}")

cv2.destroyAllWindows()
client.close()