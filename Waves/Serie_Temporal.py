import xarray as xr

archivos = [
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME0.nc",
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME6.nc",
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME12.nc",
    r"C:\Users\Santiago Elias Porto\Downloads\data\TIME18.nc"
]

# 1️⃣ Abrir cada archivo individualmente (SIN DASK)
datasets = [
    xr.open_dataset(f, engine="netcdf4", cache=False)
    for f in archivos
]

# 2️⃣ Concatenar manualmente en el eje tiempo
ds = xr.concat(datasets, dim="time")

#print(ds)

ds_flat = ds.mean(dim="time", skipna=True)
print(ds_flat)


#serie temporal en un punto

import matplotlib.pyplot as plt

swh_mean = ds_flat["swh"].mean(dim="valid_time")
pt = ds_flat["swh"].sel(
    latitude=11.55,
    longitude=-73.6,
    method="nearest"
)

pt.plot()
plt.show()
