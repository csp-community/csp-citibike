import os.path
import urllib.error
import urllib.request
import zipfile

import pandas as pd

from .common import _to_csv_files, _to_local_data_path
from .load import load_data

_BASE_URL = "https://s3.amazonaws.com/tripdata/"


_RAW_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "raw_data")


def download_data(year=None, month=None, as_df=True):
    filename, local_data_file, local_data_folder = _to_local_data_path(
        year=year, month=month
    )

    # Download zip file from s3 and extract
    if not os.path.exists(local_data_file):
        if not os.path.exists(_RAW_DATA_PATH):
            os.mkdir(_RAW_DATA_PATH)

        print("Downloading data...")
        try:
            urllib.request.urlretrieve(_BASE_URL + filename, local_data_file)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Could not find {_BASE_URL + filename}!") from exc

        if not os.path.exists(local_data_folder):
            os.mkdir(local_data_folder)

        with zipfile.ZipFile(local_data_file, "r") as zip_ref:
            zip_ref.extractall(local_data_folder)

    datapath, csvs = _to_csv_files(year=year, month=month)
    all_csv_path = os.path.join(datapath, "all.csv")

    if not os.path.exists(all_csv_path):
        df = pd.concat([pd.read_csv(os.path.join(datapath, csv)) for csv in csvs])
        df.sort_values("started_at", inplace=True)
        df.to_csv(all_csv_path, index=False)

    if as_df:
        df = pd.read_csv(all_csv_path)
        return df
    return all_csv_path
