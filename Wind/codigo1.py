import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes

# =====================================================
# 1. CARGA DE ARCHIVOS DIMAR / ERA5
# =====================================================
archivos = [
    r"C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\TIME00.nc",
    r"C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\TIME66.nc",
    r"C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\TIME1212.nc",
    r"C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\TIME1818.nc"
]

ds_list = [xr.open_dataset(f, engine="netcdf4") for f in archivos]
ds = xr.concat(ds_list, dim="valid_time")
ds = ds.sortby("valid_time")

# =====================================================
# 2. SELECCIÓN DEL PUNTO OFFSHORE
# =====================================================
ds_pt = ds.sel(
    latitude=10.99,
    longitude=-75.64,
    method="nearest"
)

u = ds_pt["u100"]
v = ds_pt["v100"]

# =====================================================
# 3. VELOCIDAD Y DIRECCIÓN DEL VIENTO
# =====================================================
vel = np.sqrt(u**2 + v**2)

# Dirección meteorológica (desde donde sopla)
dir = (270 - np.rad2deg(np.arctan2(v, u))) % 360

# =====================================================
# 4. DATAFRAME DE TRABAJO
# =====================================================
df = pd.DataFrame({
    "time": pd.to_datetime(ds_pt.valid_time.values),
    "vel": vel.values,
    "dir": dir.values
})

df["hour"] = df["time"].dt.hour
df["month"] = df["time"].dt.month
df["year"] = df["time"].dt.year

# =====================================================
# 5. POTENCIA CÚBICA (ENERGÍA EÓLICA)
# =====================================================
df["V3"] = df["vel"] ** 3

# =====================================================
# 6. PROMEDIOS MENSUALES
# =====================================================
prom_mensual = df.groupby(["year", "month"]).agg(
    V_mean=("vel", "mean"),
    V3_mean=("V3", "mean")
).reset_index()

print("\n📊 PROMEDIOS MENSUALES (2005–2025):")
print(prom_mensual.head())

# =====================================================
# 7. ROSA DE VIENTO PROFESIONAL (100 m)
# =====================================================
fig = plt.figure(figsize=(8, 8))
ax = WindroseAxes.from_ax(fig=fig)

ax.bar(
    df["dir"],
    df["vel"],
    bins=np.arange(0, 15, 2),
    normed=True,
    opening=0.9,
    edgecolor="black"
)

ax.set_legend(title="Velocidad [m/s]", loc="lower right")
ax.set_title(
    "Rosa de Viento Offshore – 100 m\nCaribe Colombiano (2005–2025)",
    fontsize=12
)

plt.show()
