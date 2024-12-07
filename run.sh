#!/bin/bash

# Caminho para o diretório local dos pacotes ROS
LOCAL_ROS_PKG_DIR=$(pwd)/ros_pkg

# Nome da imagem Docker
IMAGE_NAME="ros2-humble-with-ws"

# Execute o container
docker run -it \
    --rm \                               # Remove o container após sair
    --privileged
    --device /dev/video0:/dev/video0 \   # Dá acesso ao dispositivo de câmera
    -e DISPLAY=$DISPLAY \                # Exporta a variável DISPLAY para o container
    -v /tmp/.X11-unix:/tmp/.X11-unix \   # Monta o servidor X11 para acesso ao display
    $IMAGE_NAME \
    bash