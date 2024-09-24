import mne
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('eeg.csv')

# Seleccionar los valores de las celdas de las primeras 8 columnas
electrode_data = df.iloc[:, 0:8]

# Transponer los datos para obtener un array con dimensiones (n_channels, n_times)
data = np.transpose(electrode_data.values)

# Nombres de los electrodos según el sistema 10-20
ch_names_1020sys = ['F3','Fz', 'F4', 'C3', 'C4', 'P3', 'Pz', 'P4']

# Crear la información del montaje
info = mne.create_info(ch_names=ch_names_1020sys, sfreq=256, ch_types='eeg')

# Crear el objeto EvokedArray
evokedArr = mne.EvokedArray(data, info)

# Configurar el montaje de 10-20
ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
evokedArr.set_montage(ten_twenty_montage)

# Crear las figuras para la topografía
fig, ax = plt.subplots(1, 2, gridspec_kw=dict(width_ratios=[10, 2]))

# Ajustar los datos para la visualización
evokedArr.data /= 1000000  # Para que los colorbars sean diferentes

# Graficar la topografía
evokedArr.plot_topomap(times=0, time_unit='s', time_format=None,
                       axes=ax[:2], cmap='Spectral_r', colorbar=True,
                       show=False)

# Ajustar el título y mostrar la gráfica
ax[0].set_title('Alpha')
plt.show()
