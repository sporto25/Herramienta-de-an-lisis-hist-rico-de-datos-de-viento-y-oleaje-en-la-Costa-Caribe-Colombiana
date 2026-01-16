import xarray as xr

archivos = [
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME0.nc",
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME6.nc",
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME12.nc",
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME18.nc"
]

# 1️⃣ Abrir cada archivo individualmente (SIN DASK)
datasets = [
    xr.open_dataset(f, engine="netcdf4", cache=False)
    for f in archivos
]

# 2️⃣ Concatenar manualmente en el eje tiempo
ds = xr.concat(datasets, dim="time")

#print(ds)

ds_flat = ds.mean(dim="time", skipna=True)
print(ds_flat)


#serie temporal en un punto

import matplotlib.pyplot as plt

swh_mean = ds_flat["swh"].mean(dim="valid_time")
pt = ds_flat["swh"].sel(
    latitude=11.55,
    longitude=-73.6,
    method="nearest"
)


import numpy as np
import matplotlib.pyplot as plt

# Selecciona punto más cercano
pt = ds_flat.sel(
    latitude=11.55,
    longitude=-73.6,
    method="nearest"
)

# Extraer datos
Hs = pt["swh"].values
Dir = pt["mwd"].values

mask = np.isfinite(Hs) & np.isfinite(Dir)
Hs = Hs[mask]
Dir = Dir[mask]

# Bins de dirección (12 sectores = 30°)
dir_bins = np.arange(0, 361, 30)

# Bins de altura significativa [m]
hs_bins = [0, 1, 2, 3, 4, 5, 10]

# Ajustar dirección a sistema polar
Dir_rad = np.deg2rad(Dir)

# Histograma 2D
hist, _, _ = np.histogram2d(
    Dir,
    Hs,
    bins=[dir_bins, hs_bins]
)

# Normalizar (%)
hist = hist / hist.sum() * 100

theta = np.deg2rad((dir_bins[:-1] + dir_bins[1:]) / 2)

fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)

bottom = np.zeros(len(theta))

for i in range(len(hs_bins)-1):
    values = hist[:, i]
    ax.bar(
        theta,
        values,
        width=np.deg2rad(30),
        bottom=bottom,
        label=f"{hs_bins[i]}–{hs_bins[i+1]} m"
    )
    bottom += values

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title("Rosa de olas – Caribe Colombiano\n(Punto DIMAR)", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

plt.show()

plt.show()

