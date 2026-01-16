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
    return ds

def process(ds):
    Hs = ds["swh"]

    return {
        "Hs_mean": float(Hs.mean()),
        "Hs_max": float(Hs.max()),
        "Hs_p95": float(Hs.quantile(0.95))
    }

def plot(ds):
    Hs = ds["swh"].values.flatten()
    Dir = ds["mwd"].values.flatten()

    mask = np.isfinite(Hs) & np.isfinite(Dir)
    Hs, Dir = Hs[mask], Dir[mask]

    bins_dir = np.arange(0, 361, 30)
    bins_hs = [0,1,2,3,4,5,10]

    hist, _, _ = np.histogram2d(Dir, Hs, bins=[bins_dir, bins_hs])
    hist = hist / hist.sum() * 100

    theta = np.deg2rad((bins_dir[:-1] + bins_dir[1:]) / 2)

    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    bottom = np.zeros(len(theta))

    for i in range(len(bins_hs)-1):
        ax.bar(
            theta,
            hist[:,i],
            width=np.deg2rad(30),
            bottom=bottom,
            label=f"{bins_hs[i]}–{bins_hs[i+1]} m"
        )
        bottom += hist[:,i]

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3,1.1))
    ax.set_title("Rosa de oleaje")

    return fig
