#!/bin/bash

# Caminho para o diretório local dos pacotes ROS
LOCAL_ROS_PKG_DIR=$(pwd)/ros_pkg

# Nome da imagem Docker
IMAGE_NAME="raspicam_ros"

# Allow local connections to the X server for GUI applications in Docker
xhost +local:

# Setup for X11 forwarding to enable GUI
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

# Execute o container
docker run -it --rm --privileged --device /dev/video0:/dev/video0 -e DISPLAY=$DISPLAY \
    -v ./src:/root/ros_ws/src -v /dev:/dev --env="QT_X11_NO_MITSHM=1" \
    --name="Telecom" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --env="XAUTHORITY=$XAUTH" \
    --volume="$XAUTH:$XAUTH" $IMAGE_NAME bash