import numpy as np

def velocidad_viento(u, v):
    return np.sqrt(u**2 + v**2)

def preparar_viento(ds_point, altura=100):
    u = ds_point[f"u{altura}"].values
    v = ds_point[f"v{altura}"].values
    V = velocidad_viento(u, v)
    return V[np.isfinite(V)]
