from pathlib import Path
import pandas as pd

def get_export_path(user, zone, param):
    base = Path("exports") / user / zone / param
    base.mkdir(parents=True, exist_ok=True)
    return base


def export_stats(stats_dict, path):
    df = pd.DataFrame([stats_dict])
    df.to_csv(path / "stats.csv", index=False)


def export_netcdf(dataset, path, name="data.nc"):
    dataset.to_netcdf(path / name)


def export_figure(fig, path, name="figure.png"):
    fig.savefig(path / name, dpi=300, bbox_inches="tight")
