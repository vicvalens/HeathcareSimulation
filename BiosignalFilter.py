import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Generar una señal senoidal con ruido
def generate_signal(frequency=5, sampling_rate=100, duration=5, noise_level=0.5):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t) + noise_level * np.random.normal(size=t.shape)
    return t, signal

# Filtro pasa-bajas utilizando un filtro Butterworth
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

# Parámetros de la señal
frequency = 5       # Frecuencia de la señal en Hz
sampling_rate = 100  # Frecuencia de muestreo en Hz
duration = 5        # Duración de la señal en segundos
noise_level = 0.5   # Nivel de ruido

# Generar la señal
t, signal = generate_signal(frequency, sampling_rate, duration, noise_level)

# Parámetros del filtro
cutoff_frequency = 2.5  # Frecuencia de corte en Hz
order = 4               # Orden del filtro

# Aplicar el filtro a la señal
filtered_signal = butter_lowpass_filter(signal, cutoff_frequency, sampling_rate, order)

# Visualizar la señal original y la señal filtrada
plt.figure(figsize=(10, 6))
plt.plot(t, signal, label='Señal con ruido', alpha=0.5)
plt.plot(t, filtered_signal, label='Señal filtrada', linewidth=2)
plt.title('Procesamiento de una bioseñal simulada')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.show()
