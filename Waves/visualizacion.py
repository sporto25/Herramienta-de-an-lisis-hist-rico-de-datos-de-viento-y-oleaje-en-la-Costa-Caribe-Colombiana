import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def plot_mean_wind(ds, year):
    ds_year = ds.sel(time=str(year))
    mean_wspd = ds_year['wspd'].mean(dim='time')

    fig = plt.figure(figsize=(8,6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    mean_wspd.plot(
        ax=ax,
        cmap='viridis',
        cbar_kwargs={'label': 'Velocidad del viento (m/s)'}
    )
    ax.coastlines()
    ax.set_extent([-82, -71, 8, 13.5])
    ax.set_title(f'Viento promedio {year}')
    plt.show()

def plot_time_series(ds, lat, lon):
    pt = ds.sel(latitude=lat, longitude=lon, method='nearest')

    fig, ax = plt.subplots()
    pt['wspd'].plot(ax=ax)
    ax.set_ylabel('m/s')
    ax.set_title('Serie temporal velocidad del viento')
    plt.show()
