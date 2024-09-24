import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from scipy.interpolate import make_interp_spline

# Función para simular una onda similar a un latido del corazón (ECG)
def generate_ecg_waveform(t):
    heart_rate = 60  # Latidos por minuto
    bpm = heart_rate / 60.0  # Latidos por segundo

    # Crear una señal básica de ECG usando funciones trigonométricas y gaussianas
    ecg = 0.6 * np.sin(2 * np.pi * bpm * t)  # Onda P
    ecg += -1.2 * np.exp(-((t % (1/bpm)) - 0.2)**2 / (2 * 0.01**2))  # Complejo Q
    ecg += 3.0 * np.exp(-((t % (1/bpm)) - 0.3)**2 / (2 * 0.003**2))  # Complejo R
    ecg += -1.2 * np.exp(-((t % (1/bpm)) - 0.4)**2 / (2 * 0.01**2))  # Complejo S
    ecg += 0.4 * np.exp(-((t % (1/bpm)) - 0.6)**2 / (2 * 0.02**2))  # Onda T

    return ecg

# Función para actualizar la gráfica en tiempo real
def update_wave(i, xs, ys, line, ax, color):
    t = xs[-1] + 0.01  # Incrementar el tiempo
    amplitude = generate_ecg_waveform(t)
    xs.append(t)
    ys.append(amplitude)

    # Mantener solo los últimos 100 puntos para un gráfico de desplazamiento
    xs = xs[-100:]
    ys = ys[-100:]

    # Suavizar la onda
    if len(xs) > 3:
        xnew = np.linspace(min(xs), max(xs), 300)
        spl = make_interp_spline(xs, ys, k=3)
        y_smooth = spl(xnew)
        line.set_data(xnew, y_smooth)
        ax.set_xlim(min(xs), max(xs))
        ax.set_ylim(min(y_smooth), max(y_smooth))
    else:
        line.set_data(xs, ys)
        ax.set_xlim(min(xs), max(xs))
        ax.set_ylim(min(ys), max(ys))

    return line,

# Función para configurar y mostrar la gráfica
def plot_wave(color='blue'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title('Simulación de la Onda ECG')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud')
    ax.grid(True)
    
    xs, ys = [0], [generate_ecg_waveform(0)]
    line, = ax.plot([], [], color=color, linestyle='-', linewidth=2)
    
    ani = animation.FuncAnimation(
        fig, update_wave, fargs=(xs, ys, line, ax, color), interval=50, blit=True, cache_frame_data=False
    )
    
    plt.show()

# Ejecutar la visualización de la onda en tiempo real
plot_wave(color='red')  # Cambia 'red' al color que prefieras
