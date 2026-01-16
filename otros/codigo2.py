# =====================================================
# ANÁLISIS EÓLICO OFFSHORE – CNO 1768 COMPLIANT
# Caribe Colombiano – 100 m
# =====================================================

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes

# =====================================================
# 1. CARGA DE ARCHIVOS (DIMAR / ERA5)
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
# 2. SELECCIÓN DEL PUNTO OFFSHORE (POR COORDENADAS)
# =====================================================
ds_pt = ds.sel(
    latitude=10.99,
    longitude=-75.64,
    method="nearest"
)

u = ds_pt["u100"]
v = ds_pt["v100"]

# =====================================================
# 3. VARIABLES PRIMARIAS (BASE FÍSICA)
# =====================================================
vel = np.sqrt(u**2 + v**2)

dir = (270 - np.rad2deg(np.arctan2(v, u))) % 360

# =====================================================
# 4. DATAFRAME BASE (SERIE ORIGINAL 0–6–12–18)
# =====================================================
df = pd.DataFrame({
    "time": pd.to_datetime(ds_pt.valid_time.values),
    "u": u.values,
    "v": v.values,
    "vel": vel.values,
    "dir": dir.values
}).set_index("time").sort_index()

# =====================================================
# 5. POTENCIA CÚBICA (VARIABLE ENERGÉTICA)
#    >>> VARIABLE A INTERPOLAR SEGÚN CNO 1768 <<<
# =====================================================
df["V3"] = df["vel"] ** 3

# =====================================================
# 6. CONSTRUCCIÓN DE EJE HORARIO COMPLETO
# =====================================================
idx_horario = pd.date_range(
    start=df.index.min(),
    end=df.index.max(),
    freq="1H"
)

df_h = df.reindex(idx_horario)

# =====================================================
# 7. INTERPOLACIÓN NORMATIVA (CNO 1768)
#    ✔ SOLO V³
#    ✔ LINEAL
# =====================================================
df_h["V3_interp"] = df_h["V3"].interpolate(
    method="linear",
    limit_direction="both"
)

# =====================================================
# 8. RECONSTRUCCIÓN DE VELOCIDAD HORARIA
# =====================================================
df_h["vel_interp"] = df_h["V3_interp"] ** (1/3)

# =====================================================
# 9. TRATAMIENTO DE DIRECCIÓN (SIN INTERPOLAR)
#    → Dirección constante por bloque de 6 h
# =====================================================
df_h["dir_interp"] = (
    df["dir"]
    .resample("6H")
    .ffill()
    .reindex(idx_horario, method="ffill")
)

# =====================================================
# 10. VARIABLES TEMPORALES
# =====================================================
df_h["hour"] = df_h.index.hour
df_h["month"] = df_h.index.month
df_h["year"] = df_h.index.year

# =====================================================
# 11. PROMEDIOS MENSUALES ENERGÉTICOS (CNO)
# =====================================================
prom_mensual = df_h.groupby(["year", "month"]).agg(
    V_mean=("vel_interp", "mean"),
    V3_mean=("V3_interp", "mean")
).reset_index()

print("\n📊 PROMEDIOS MENSUALES (CNO 1768):")
print(prom_mensual.head())

# =====================================================
# 12. ROSA DE VIENTO HORARIA EQUIVALENTE (100 m)
# =====================================================
fig = plt.figure(figsize=(8, 8))
ax = WindroseAxes.from_ax(fig=fig)

ax.bar(
    df_h["dir_interp"],
    df_h["vel_interp"],
    bins=[0,4,6,8,10,12,15],
    nsector=16,
    normed=True,
    opening=0.9,
    edgecolor="black"
)

ax.set_yticks([5, 10, 20, 30, 40])
ax.set_yticklabels(["5%", "10%", "20%", "30%", "40%"])

ax.set_legend(title="Velocidad [m/s]", loc="lower right")

ax.set_title(
    "Rosa de Viento Offshore – 100 m\n"
    "Interpolación energética (CNO 1768)\n"
    "Caribe Colombiano (2005–2025)",
    fontsize=11
)

plt.show()
