import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from glob import glob

# =========================
# LOAD DATA
# =========================
def load_data(path):
    files = glob(f"{path}/*.nc")

    ds = xr.open_mfdataset(
        files,
        combine="nested",
        concat_dim="points"
    )

    return ds

# =========================
# PROCESS
# =========================
def process(ds):
    depth = ds["wmb"].values

    return {
        "min": float(np.nanmin(depth)),
        "max": float(np.nanmax(depth)),
        "mean": float(np.nanmean(depth)),
        "N": int(np.isfinite(depth).sum())
    }

# =========================
# PLOT
# =========================
def plot(ds):
    depth = ds["wmb"].values.flatten()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(depth, linewidth=0.8)
    ax.set_title("Perfil de Batimetría")
    ax.set_xlabel("Índice del punto")
    ax.set_ylabel("Profundidad [m]")
    ax.grid(True)

    return fig

