import xarray as xr
import numpy as np

archivos = [
    r"C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\TIME00.nc",
    r"C:\Users\Santiago Elias Porto\Desktop\dataCosta\DIMAR-CostaEolica\TIME66.nc"
]

# Abrir archivos individualmente
ds_list = [xr.open_dataset(f, engine="netcdf4") for f in archivos]

# Unir por dimensión temporal
ds = xr.concat(ds_list, dim="valid_time")

# Ordenar el tiempo (CLAVE)
ds = ds.sortby("valid_time")

print(ds)
print(ds.dims)
print(list(ds.data_vars))
print(ds.coords)
