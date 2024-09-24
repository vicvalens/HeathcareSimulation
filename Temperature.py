import tkinter as tk
from tkinter import ttk
import random
import time
import threading
import winsound  # Solo disponible en Windows

# Función para simular la obtención de la temperatura corporal
def get_body_temperature():
    # Simular una temperatura corporal con posible fiebre
    return round(random.uniform(36.0, 39.0), 1)

# Función para reproducir un sonido de alarma
def play_alarm_sound():
    frequency = 1000  # Frecuencia del sonido en Hz
    duration = 500    # Duración del sonido en milisegundos
    winsound.Beep(frequency, duration)

# Función para actualizar la temperatura en la interfaz
def update_temperature(label, root):
    while True:
        temp = get_body_temperature()
        label.config(text=f"{temp} °C")
        
        # Cambiar el color de fondo en función de la temperatura
        if temp >= 37.5:
            label.config(foreground="red")
            root.config(bg="lightcoral")
            play_alarm_sound()
        else:
            label.config(foreground="black")
            root.config(bg="lightgreen")
        
        time.sleep(1)  # Actualizar cada segundo

# Configuración de la interfaz gráfica
def create_interface():
    root = tk.Tk()
    root.title("Monitor de Temperatura Corporal")
    root.geometry("400x200")

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 48))

    # Crear una etiqueta para mostrar la temperatura
    temp_label = ttk.Label(root, text="36.5 °C", style="TLabel")
    temp_label.pack(pady=50)

    # Configurar el color de fondo inicial
    root.config(bg="lightgreen")

    # Crear un hilo para actualizar la temperatura
    thread = threading.Thread(target=update_temperature, args=(temp_label, root))
    thread.daemon = True
    thread.start()

    # Iniciar la interfaz gráfica
    root.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    create_interface()
