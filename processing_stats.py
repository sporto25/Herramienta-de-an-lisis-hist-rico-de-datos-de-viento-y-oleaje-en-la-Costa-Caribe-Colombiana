import numpy as np

def estadisticas_generales(data):
    return {
        "media": float(np.mean(data)),
        "max": float(np.max(data)),
        "min": float(np.min(data)),
        "p95": float(np.percentile(data, 95)),
        "registros": int(len(data))
    }
