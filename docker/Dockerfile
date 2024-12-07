# Use a imagem base do ROS 2 Humble Desktop
FROM osrf/ros:humble-desktop-full
# FROM arm64v8/ros:humble

# Defina o maintainer (opcional)
LABEL maintainer="seu-email@exemplo.com"

# Atualize os pacotes e instale dependências gerais
RUN apt-get update && apt-get install -y \
    python3-pip \
    libopencv-dev \
    python3-opencv \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instale o opencv-python via pip
RUN pip3 install opencv-python && pip install picamera

RUN mkdir -p ~/ros_ws/src
COPY ./src ~/ros_ws/src

RUN bash -c "cd ~/ros_ws && colcon build --symlink-install"
# Defina o entrypoint padrão para o ROS 2
CMD ["bash"]