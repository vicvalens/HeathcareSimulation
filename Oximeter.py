import tkinter as tk
from tkinter import ttk
import random
import winsound
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para simular la obtención de SpO2 y heart rate
def get_oximeter_readings():
    spo2 = random.randint(90, 100)  # Simulación de SpO2 entre 90% y 100%
    heart_rate = random.randint(50, 120)  # Simulación de frecuencia cardíaca
    return spo2, heart_rate

# Función para reproducir un sonido de alarma
def play_alarm_sound():
    frequency = 1000  # Frecuencia del sonido en Hz
    duration = 500    # Duración del sonido en milisegundos
    winsound.Beep(frequency, duration)

# Función para actualizar los valores del oxímetro en la interfaz
def update_oximeter(label_spo2, label_hr, root):
    try:
        if not label_spo2.winfo_exists() or not label_hr.winfo_exists() or not root.winfo_exists():
            return  # Si el widget ha sido destruido, salimos de la función

        spo2, heart_rate = get_oximeter_readings()
        label_spo2.config(text=f"SpO2: {spo2} %")
        label_hr.config(text=f"Heart Rate: {heart_rate} BPM")
        
        # Cambiar el color de fondo en función de las lecturas
        if spo2 < 95:
            label_spo2.config(foreground="red")
            play_alarm_sound()
        else:
            label_spo2.config(foreground="black")

        if heart_rate < 60 or heart_rate > 100:
            label_hr.config(foreground="red")
            play_alarm_sound()
        else:
            label_hr.config(foreground="black")

        # Asegurar que el root aún existe antes de reprogramar la llamada
        if root.winfo_exists():
            root.after(1000, update_oximeter, label_spo2, label_hr, root)
    except Exception as e:
        print(f"Error updating oximeter readings: {e}")

# Función para manejar el cierre seguro de la ventana
def on_closing(root):
    if root.winfo_exists():
        root.quit()
        root.destroy()

# Configuración de la interfaz gráfica
def create_interface():
    root = tk.Tk()
    root.title("Simulador de Oxímetro")
    root.geometry("400x300")

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 32))

    # Crear etiquetas para mostrar SpO2 y frecuencia cardíaca
    spo2_label = ttk.Label(root, text="SpO2: -- %", style="TLabel")
    spo2_label.pack(pady=20)

    heart_rate_label = ttk.Label(root, text="Heart Rate: -- BPM", style="TLabel")
    heart_rate_label.pack(pady=20)

    # Configurar el color de fondo inicial
    root.config(bg="lightgreen")

    # Iniciar la primera actualización del oxímetro
    root.after(1000, update_oximeter, spo2_label, heart_rate_label, root)

    # Manejar el cierre de la ventana para detener las actualizaciones pendientes
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Iniciar la interfaz gráfica
    root.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    create_interface()
