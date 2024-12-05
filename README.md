

1. Ping (Latência):
O tempo de resposta entre o cliente e o servidor.

2. Jitter (Variação no atraso)
Mede a variabilidade do tempo de chegada dos pacotes. No streaming de vídeo, um jitter alto pode causar interrupções e atrasos. medir o tempo de chegada de cada pacote (recv_time) e calcular a diferença em relação ao pacote anterior.

3. Taxa de Quadros Recebidos (FPS Real)
Mede quantos quadros por segundo estão sendo exibidos no cliente, que pode ser diferente do FPS capturado pelo servidor devido a perdas e atrasos. Conta quantos frames foram recebidos em 1 segundo:

4. Latência de Transmissão (End-to-End Latency)
Mede o tempo total para um quadro ser capturado no servidor e exibido no cliente. Incluir um timestamp no pacote do servidor (usando time.time()), envie com cada frame e subtraia o tempo atual no cliente quando o frame for recebido. #EM DESENVOLVIMENTO

5. Desempenho da Decodificação
Mede o tempo gasto pelo cliente para decodificar e exibir cada quadro. Usa o time.time() antes e depois de cv2.imdecode e registra o tempo médio.

6. Utilização da Rede (Network Utilization)
Mede o quanto da capacidade da rede está sendo utilizada pela aplicação. Compara a largura de banda atual com a largura de banda total disponível.