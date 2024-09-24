import tkinter as tk
import numpy as np
from pylsl import StreamInlet, StreamInfo, StreamOutlet, resolve_stream
from scipy.signal import butter, lfilter
import time

# Funciones para crear y aplicar filtros de banda
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Mapa de colores basados en el nivel de relajación (RGB)
color_map = {
    'low_relaxation': (199, 21, 133),      # Magenta
    'medium_relaxation': (148, 0, 211),    # Violeta
    'high_relaxation': (0, 191, 255),      # Azul
    'very_high_relaxation': (245, 245, 245) # Blanco
}

# Función para convertir RGB a color hexadecimal
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Parámetros del filtro
fs = 100  # Frecuencia de muestreo (ajustar según tus datos)
lowcut_alpha = 8.0
highcut_alpha = 12.0
lowcut_theta = 4.0
highcut_theta = 8.0

# Resolver el stream de AURA_Power
print("Buscando el stream 'AURA_Power'...")
streams = resolve_stream('name', 'AURA_Power')

# Crear un nuevo stream LSL para enviar triggers con un ID de fuente único
info = StreamInfo('eeg_stream', 'Markers', 1, 0, 'string', 'unique_source_id_eeg_stream_001')
outlet = StreamOutlet(info)

# Crear un inlet para el stream AURA_Power
inlet = StreamInlet(streams[0])

def send_trigger(trigger_name):
    outlet.push_sample([trigger_name])
    print(f'Trigger enviado: {trigger_name}')

# Mapa de triggers basados en el índice de relajación
def determine_trigger(value):
    if value < 0.1:
        return 'low_relaxation'
    elif value < 0.3:
        return 'medium_relaxation'
    elif value < 0.5:
        return 'high_relaxation'
    else:
        return 'very_high_relaxation'

# Función para hacer la transición suave de color
def smooth_transition(current_color, target_color, steps=20, delay=0.05):
    r1, g1, b1 = current_color
    r2, g2, b2 = target_color

    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)

        hex_color = rgb_to_hex((r, g, b))
        root.config(bg=hex_color)
        root.update()
        time.sleep(delay)

# Configuración de la interfaz gráfica con tkinter
root = tk.Tk()
root.title("Monitor de Relajación")
root.geometry("400x400")

# Iniciar la interfaz gráfica en un color neutro
current_color = (128, 128, 128)  # Gris
root.config(bg=rgb_to_hex(current_color))

# Iniciar el proceso de adquisición de datos
print("Recibiendo datos del stream 'AURA_Power'...")
eeg_data = []

while True:
    sample, timestamp = inlet.pull_sample()
    if sample:
        eeg_data.append(sample[:40])  # Suponiendo que sample contiene 8 valores de los electrodos de EEG

        if len(eeg_data) >= fs * 1:  # Procesar cada segundo
            eeg_data_np = np.array(eeg_data)
            eeg_data = []  # Reiniciar el buffer

            alpha_power = np.mean([np.sum(bandpass_filter(eeg_data_np[:, i], lowcut_alpha, highcut_alpha, fs)**2) for i in range(8)])
            theta_power = np.mean([np.sum(bandpass_filter(eeg_data_np[:, i], lowcut_theta, highcut_theta, fs)**2) for i in range(8)])

            relaxation_index = alpha_power / theta_power  # Índice simplificado de relajación

            print(f"Alpha Power: {alpha_power}, Theta Power: {theta_power}, Relaxation Index: {relaxation_index}")

            trigger = determine_trigger(relaxation_index)
            send_trigger(trigger)

            target_color = color_map[trigger]
            smooth_transition(current_color, target_color)
            current_color = target_color  # Actualizar el color actual
