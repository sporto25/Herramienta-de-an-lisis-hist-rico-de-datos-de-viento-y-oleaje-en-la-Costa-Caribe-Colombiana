import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import glob

def load_data(path):
    files = sorted(glob.glob(f"{path}/*.nc"))
    ds = xr.open_mfdataset(
        files,
        combine="nested",
        concat_dim="valid_time"
    ).sortby("valid_time")
    print(ds)
    return ds

def process(ds):
    u = ds["u100"]
    v = ds["v100"]
    speed = np.sqrt(u**2 + v**2)

    return {
        "mean": float(speed.mean()),
        "max": float(speed.max()),
        "p95": float(speed.quantile(0.95))
    }

def plot(ds):
    u = ds["u100"]
    v = ds["v100"]
    speed = np.sqrt(u**2 + v**2)

    fig, ax = plt.subplots(figsize=(8,3))
    speed.mean(dim=["latitude","longitude"]).plot(ax=ax)
    ax.set_title("Velocidad del viento a 100 m")

    return fig
