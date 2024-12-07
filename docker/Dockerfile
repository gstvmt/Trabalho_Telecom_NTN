# Use a imagem base do ROS 2 Humble Desktop
FROM ros:humble-desktop

# Defina o maintainer (opcional)
LABEL maintainer="seu-email@exemplo.com"

# Atualize os pacotes e instale as dependências necessárias
RUN apt-get update && apt-get install -y \
    python3-picamera \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN rosdep install -i --from-path src --rosdistro humble -y

RUN mkdir -p /ros_ws
COPY ./src /ros_ws/

RUN bash -c "cd ros_ws && colcon build --sylink-install"
# Defina o entrypoint padrão para o ROS 2
CMD ["bash"]