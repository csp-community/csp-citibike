import os.path

import pandas as pd

from .common import _to_csv_files


def load_data(year=None, month=None):
    datapath, csvs = _to_csv_files(year=year, month=month)
    if os.path.exists(os.path.join(datapath, "all.csv")):
        return pd.read_csv(os.path.join(datapath, "all.csv"))
    return pd.concat([pd.read_csv(os.path.join(datapath, csv)) for csv in csvs])
