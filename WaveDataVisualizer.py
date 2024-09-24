import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Función para leer datos desde un archivo CSV
def read_wave_data(filename):
    times = []
    amplitudes = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            times.append(float(row['Time']))
            amplitudes.append(float(row['Amplitude']))
    return times, amplitudes

# Función para visualizar los datos de la onda con suavizado
def plot_wave(filename, color='blue'):
    times, amplitudes = read_wave_data(filename)
    
    # Suavizar la onda
    xnew = np.linspace(min(times), max(times), 300)
    spl = make_interp_spline(times, amplitudes, k=3)  # B-spline interpolación cúbica
    y_smooth = spl(xnew)
    
    # Configurar la visualización
    plt.figure(figsize=(10, 6))
    plt.plot(xnew, y_smooth, color=color, linestyle='-', linewidth=2)
    plt.title('Visualización de la Onda Suavizada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Archivo CSV de entrada
filename = 'wave_data.csv'

# Ejecutar la visualización de la onda
plot_wave(filename, color='purple')  # Cambia 'red' al color que prefieras
