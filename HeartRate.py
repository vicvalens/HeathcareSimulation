import tkinter as tk
from tkinter import ttk
import random
import winsound
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import make_interp_spline

# Función para simular la obtención del heart rate
def get_heart_rate():
    return random.randint(50, 120)

# Función para reproducir un sonido de alarma
def play_alarm_sound():
    frequency = 1000  # Frecuencia del sonido en Hz
    duration = 500    # Duración del sonido en milisegundos
    winsound.Beep(frequency, duration)

# Función para actualizar la frecuencia cardíaca en la interfaz
def update_heart_rate(label, root):
    try:
        if not label.winfo_exists() or not root.winfo_exists():
            return  # Si el widget ha sido destruido, salimos de la función

        heart_rate = get_heart_rate()
        label.config(text=f"{heart_rate} BPM")
        
        # Cambiar el color de fondo en función de la frecuencia cardíaca
        if heart_rate < 60:
            label.config(foreground="blue")
            root.config(bg="lightblue")
            play_alarm_sound()
        elif heart_rate > 100:
            label.config(foreground="red")
            root.config(bg="lightcoral")
            play_alarm_sound()
        else:
            label.config(foreground="black")
            root.config(bg="lightgreen")

        # Asegurar que el root aún existe antes de reprogramar la llamada
        if root.winfo_exists():
            root.after(1000, update_heart_rate, label, root)
    except Exception as e:
        print(f"Error updating heart rate: {e}")

# Función para manejar el cierre seguro de la ventana
def on_closing(root):
    if root.winfo_exists():
        root.quit()
        root.destroy()

# Configuración de la interfaz gráfica
def create_interface():
    root = tk.Tk()
    root.title("Monitor de Ritmo Cardíaco")
    root.geometry("600x400")

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 48))

    # Crear una etiqueta para mostrar el ritmo cardíaco
    heart_rate_label = ttk.Label(root, text="75 BPM", style="TLabel")
    heart_rate_label.pack(pady=20)

    # Configurar el color de fondo inicial
    root.config(bg="lightgreen")

    # Iniciar la primera actualización de la frecuencia cardíaca
    root.after(1000, update_heart_rate, heart_rate_label, root)

    # Crear la figura para la gráfica tipo ECG
    fig, ax = plt.subplots()
    xs = list(range(100))  # Tiempo ficticio
    ys = [0] * 100  # Valores iniciales de ECG ficticio

    # Función para actualizar la gráfica
    def animate(i, xs, ys):
        try:
            if not root.winfo_exists():
                return  # Si la ventana ha sido destruida, salimos de la función

            # Simula el próximo punto del ECG
            next_value = random.choice([0, 0.5, 1, 0.5, 0, -0.5, -1, -0.5, 0])
            ys.append(next_value)
            ys = ys[-100:]

            ax.clear()

            # Suavizar la línea de la gráfica
            xnew = np.linspace(min(xs), max(xs), 300)  # Nuevos puntos de x
            spl = make_interp_spline(xs, ys, k=3)  # B-Spline para suavizar
            y_smooth = spl(xnew)

            ax.plot(xnew, y_smooth, linestyle='-', linewidth=2)  # Gráfica suavizada
            ax.set_ylim([-1.5, 1.5])
            ax.set_title("Simulación de ECG")
            ax.set_ylabel("Amplitud")
            ax.set_xlabel("Tiempo")
        except Exception as e:
            print(f"Error in animation: {e}")

    # Configurar la animación
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100, cache_frame_data=False)

    # Integrar la gráfica de ECG en tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Manejar el cierre de la ventana para detener las actualizaciones pendientes
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Iniciar la interfaz gráfica
    root.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    create_interface()
