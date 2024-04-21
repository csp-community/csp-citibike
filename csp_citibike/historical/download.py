import calendar
import os.path
import urllib.error
import urllib.request
import zipfile
from datetime import date

import pandas as pd

_BASE_URL = "https://s3.amazonaws.com/tripdata/"
_PATH_PRIOR_YEARS = "{year}-citibike-tripdata.zip"
_PATH_CURRENT_YEAR = "{year}{month}-citibike-tripdata.csv.zip"


_RAW_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "raw_data")


def download_data(year=None, month=None):
    year = year or date.today().year
    month = month or (date.today().month - 1)

    # Grab the correct file
    if int(year) == date.today().year:
        filename = _PATH_CURRENT_YEAR.format(year=year, month=str(month).zfill(2))
        local_data_file = os.path.join(_RAW_DATA_PATH, filename)
        local_data_folder = local_data_file.replace(".zip", "").replace(".csv", "")
    else:
        filename = _PATH_PRIOR_YEARS.format(year=year)
        local_data_file = os.path.join(_RAW_DATA_PATH, filename)
        local_data_folder = _RAW_DATA_PATH

    # Download zip file from s3 and extract
    if not os.path.exists(local_data_file):
        if not os.path.exists(_RAW_DATA_PATH):
            os.mkdir(_RAW_DATA_PATH)

        try:
            urllib.request.urlretrieve(_BASE_URL + filename, local_data_file)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Could not find {_BASE_URL + filename}!") from exc

        if not os.path.exists(local_data_folder):
            os.mkdir(local_data_folder)

        with zipfile.ZipFile(local_data_file, "r") as zip_ref:
            zip_ref.extractall(local_data_folder)

    # Read the csv file/s
    if int(year) == date.today().year:
        # data path is like "filename / <csvs>
        datapath = local_data_folder
    else:
        # data path is like "filename without csv / 4_April / <csvs>"
        datapath = os.path.join(
            local_data_folder,
            filename.replace(".zip", ""),
            f"{month}_{calendar.month_name[month]}",
        )

    csvs = os.listdir(os.path.join(_RAW_DATA_PATH, datapath))
    dfs = [pd.read_csv(os.path.join(datapath, csv)) for csv in csvs]
    return pd.concat(dfs)
