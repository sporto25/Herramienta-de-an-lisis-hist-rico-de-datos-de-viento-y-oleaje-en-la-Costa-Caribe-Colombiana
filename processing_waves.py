import numpy as np

def preparar_oleaje(ds_point):
    Hs = ds_point["swh"].values
    Dir = ds_point["mwd"].values
    mask = np.isfinite(Hs) & np.isfinite(Dir)
    return Hs[mask], Dir[mask]

def estadisticos_oleaje(Hs):
    return {
        "media": float(np.mean(Hs)),
        "max": float(np.max(Hs)),
        "p95": float(np.percentile(Hs, 95)),
        "registros": int(len(Hs))
    }
