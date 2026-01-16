import json
import pyproj
import numpy as np
#cargar archivo
with open(r'C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\Area 1.json', 'r') as f:
    geo = json.load(f)
   
coords_lonlat  = geo['features'][0]['geometry']['coordinates'][0] 

#proyeccion WGS84 a UTM
proj_utm = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32618", always_xy=True)

coords_utm = np.array([proj_utm.transform(lon, lat) for lon, lat in coords_lonlat])

x  = coords_utm[:,0]
y  = coords_utm[:,1]

#definir el dominio numerico real

x_min, x_max = x.min(), x.max()
y_min, y_max = y.min(), y.max()

Lx = x_max - x_min
Ly = y_max - y_min

sigma = 0.15 * min(Lx, Ly) 

dx = sigma / 10
nx = int(Lx / dx)
ny = int(Ly / dx)

x_peak_1 = 0.5 * (x_min + x_max)
y_peak_1 = 0.5 * (y_min + y_max)
x_peak_2 = x_peak_1 + 3 * sigma
y_peak_2 = y_peak_1 - 2 * sigma

A1 = 700     # zona menos profunda
A2 = -1100    # zona mas profunda
z0 = -800    # nivel base

xg = np.linspace(x_min, x_max, nx)
yg = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(xg, yg)

d1 = np.sqrt((X - x_peak_1)**2 + (Y - y_peak_1)**2)
d2 = np.sqrt((X - x_peak_2)**2 + (Y - y_peak_2)**2)

g = (
    A1 * np.exp(-(d1**2) / (2 * sigma**2)) +
    A2 * np.exp(-(d2**2) / (2 * sigma**2)) +
    z0
)

from scipy.interpolate import RegularGridInterpolator

f = RegularGridInterpolator(
    (yg, xg), g,
    bounds_error=False,
    fill_value=np.nan
)

print("\n=== RESULTADOS DEL ÁREA DE ESTUDIO ===\n")
print(f"x_min = {x_min:,.1f} m")
print(f"x_max = {x_max:,.1f} m")
print(f"Lx    = {Lx/1000:.2f} km\n")

print(f"y_min = {y_min:,.1f} m")
print(f"y_max = {y_max:,.1f} m")
print(f"Ly    = {Ly/1000:.2f} km\n")

print(f"σ recomendado = {sigma:,.1f} m")
print(f"Rango sugerido σ = [{0.1*min(Lx,Ly):,.0f} , {0.25*min(Lx,Ly):,.0f}] m")

