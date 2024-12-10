# Publisher e Subscriber de Imagem para ROS2

Este projeto contém dois scripts principais que demonstram a publicação e a assinatura de mensagens de vídeo utilizando ROS 2. Abaixo, você encontrará uma breve descrição de cada script, juntamente com links para acessá-los.

## Scripts

1. **Image Publisher (image_publisher.py)**
   - Este script publica quadros de vídeo capturados de uma câmera conectada no tópico `jetson_webcam`. Ele usa o `cv_bridge` para converter os quadros do OpenCV para o formato de imagem ROS.
   - [Veja o script Image Publisher](src/opencv_tools/opencv_tools/image_publisher.py)

2. **Image Subscriber (image_subscriber.py)**
   - Este script assina o tópico `jetson_webcam` para receber as mensagens de vídeo publicadas pelo `image_publisher.py`. Ele usa `cv_bridge` para converter a mensagem de imagem recebida para o formato OpenCV e exibe os quadros em uma janela chamada "camera".
   - [Veja o script Image Subscriber](src/opencv_tools/opencv_tools/image_subscriber.py)

## Docker

Para facilitar o ambiente de testes, um `Dockerfile` foi fornecido. Ele utiliza uma imagem base ROS2, permitindo que você construa e execute os scripts acima em um contêiner Docker.

### Dockerfile

- O `Dockerfile` configura o ambiente necessário para rodar os scripts com ROS 2.
- Ele instala as dependências necessárias, como o `cv_bridge` e o OpenCV, para garantir que os scripts funcionem corretamente.

### Script de Execução (run.sh)

- O script `run.sh` automatiza o processo de construção e execução do Docker. Depois de construir a imagem Docker com o `Dockerfile`, você pode usar o `run.sh` para executar o contêiner e testar os scripts.

## Como Usar

1. **Construir a imagem Docker:**
   - No diretório onde o `Dockerfile` está localizado, execute o seguinte comando para construir a imagem Docker:
     ```bash
     docker build -t raspicam_ros .
     ```

2. **Executar o contêiner:**
   - Após a construção da imagem, você pode executar o contêiner com o seguinte comando:
     ```bash
     ./run.sh
     ```

   Isso irá iniciar o contêiner e executar os scripts no ambiente ROS 2, permitindo que você teste a publicação e assinatura das imagens de vídeo.

## Pré-requisitos

- Docker instalado e configurado na sua máquina.
- Câmera conectada à máquina para capturar as imagens.
- ROS 2 instalado no contêiner (já configurado no `Dockerfile`).
