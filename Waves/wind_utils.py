import xarray as xr
import numpy as np

def load_dataset(path_nc):
    return xr.open_dataset(
        path_nc,
        engine="netcdf4",
        cache=False
    )


def subset_caribe_dimar(ds):
    return ds.sel(
        latitude=slice(13.5, 8.0),
        longitude=slice(-82.0, -71.0)
    )

def compute_wind_speed(ds):
    u = ds['u10']
    v = ds['v10']
    ds['wspd'] = np.sqrt(u**2 + v**2)
    return ds

def compute_wind_direction(ds):
    u = ds['u10']
    v = ds['v10']
    ds['wdir'] = (270 - np.degrees(np.arctan2(v, u))) % 360
    return ds
