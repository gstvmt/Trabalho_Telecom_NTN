import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_fft_1d(image_path):
    """
    Calcula a Transformada de Fourier 2D de uma imagem e reduz para 1D.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Imagem não encontrada: {image_path}")

    # Transformada de Fourier 2D e deslocamento para o centro
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)

    # Espectro de magnitude e fase
    magnitude = 20*np.log(np.abs(dft_shift) + 1)
    phase = np.angle(dft_shift)

    # Reduzindo para 1D (linha central da imagem)
    center_row = magnitude.shape[0] // 2
    freq = np.fft.fftfreq(img.shape[1])  # Frequência normalizada
    freq = np.fft.fftshift(freq)  # Centralizar as frequências

    return freq, magnitude[center_row, :], phase[center_row, :]

def plot_frequency_response(original_path, processed_path):
    """
    Plota magnitude e fase em função da frequência para duas imagens.
    """
    # FFT para as imagens
    freq1, mag1, phase1 = calculate_fft_1d(original_path)
    freq2, mag2, phase2 = calculate_fft_1d(processed_path)

    plt.figure(figsize=(12, 10))

    # Magnitude
    plt.subplot(2, 1, 1)
    plt.plot(freq1, mag1, label="Original", color="blue")
    plt.plot(freq2, mag2, label="Processada", color="orange")
    plt.title("Magnitude vs. Frequência")
    plt.xlabel("Frequência Normalizada")
    plt.ylabel("Magnitude (log)")
    plt.legend()
    plt.grid()

    # Fase
    plt.subplot(2, 1, 2)
    plt.plot(freq1, phase1, label="Original", color="blue")
    plt.plot(freq2, phase2, label="Processada", color="orange")
    plt.title("Fase vs. Frequência")
    plt.xlabel("Frequência Normalizada")
    plt.ylabel("Fase (radianos)")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


# Caminhos das imagens
original_image_path = "laptop/frames_client/frame_4.jpg"
processed_image_path = "raspi/frames_server/frame_4.jpg"

# Comparar resposta em frequência
plot_frequency_response(original_image_path, processed_image_path)
