import csv
import time
import math
import numpy as np

# Función para simular una onda similar a un latido del corazón (ECG)
def generate_ecg_waveform(t):
    # Definir las características básicas de un latido
    heart_rate = 60  # Latidos por minuto
    bpm = heart_rate / 60.0  # Latidos por segundo

    # Crear una señal básica de ECG usando funciones trigonométricas y gaussianas
    ecg = 0.6 * np.sin(2 * np.pi * bpm * t)  # Onda P
    ecg += -1.2 * np.exp(-((t % (1/bpm)) - 0.2)**2 / (2 * 0.01**2))  # Complejo Q
    ecg += 3.0 * np.exp(-((t % (1/bpm)) - 0.3)**2 / (2 * 0.003**2))  # Complejo R
    ecg += -1.2 * np.exp(-((t % (1/bpm)) - 0.4)**2 / (2 * 0.01**2))  # Complejo S
    ecg += 0.4 * np.exp(-((t % (1/bpm)) - 0.6)**2 / (2 * 0.02**2))  # Onda T

    return ecg

# Función para generar datos de la onda ECG y guardarlos en un archivo CSV
def generate_wave_data(filename, duration=10):
    start_time = time.time()  # Registrar el tiempo de inicio

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Amplitude'])  # Encabezado del CSV

        t = 0
        while time.time() - start_time < duration:  # Ejecutar durante 'duration' segundos
            amplitude = generate_ecg_waveform(t)
            writer.writerow([t, amplitude])

            t += 0.01  # Incremento de tiempo pequeño para una señal más detallada
            time.sleep(0.01)  # Simula la generación de datos en tiempo real

# Ejecutar la generación de datos en un archivo CSV
if __name__ == "__main__":
    filename = 'wave_data.csv'
    generate_wave_data(filename, duration=5)  # El código se detendrá después de los segundos
