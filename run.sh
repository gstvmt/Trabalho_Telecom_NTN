#!/bin/bash

# Caminho para o diretório local dos pacotes ROS
LOCAL_ROS_PKG_DIR=$(pwd)/ros_pkg

# Nome da imagem Docker
IMAGE_NAME="raspicam_ros"

# Execute o container
docker run -it --rm --privileged --device /dev/video0:/dev/video0 -e DISPLAY=$DISPLAY -v ./src:/root/ros_ws/src -v /dev:/dev $IMAGE_NAME bash