import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, std_dev=25):
    """
    Adiciona ruído Gaussiano à imagem.
    Args:
        image: Imagem original (array numpy).
        mean: Média do ruído.
        std_dev: Desvio padrão do ruído.
    Returns:
        Imagem com ruído adicionado.
    """
    noise = np.random.normal(mean, std_dev, image.shape).astype(np.float32)
    noisy_image = cv2.add(image.astype(np.float32), noise)
    return np.clip(noisy_image, 0, 255).astype(np.uint8)