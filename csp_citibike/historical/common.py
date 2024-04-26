import calendar
import os.path
from datetime import date
from functools import lru_cache

_PATH_PRIOR_YEARS = "{year}-citibike-tripdata.zip"
_PATH_CURRENT_YEAR = "{year}{month}-citibike-tripdata.csv.zip"
_RAW_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "raw_data")

__all__ = (
    "_to_local_data_path",
    "_to_csv_files",
)


@lru_cache
def _to_local_data_path(year=None, month=None):
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

    return filename, local_data_file, local_data_folder


def _to_csv_files(year=None, month=None):
    filename, _, local_data_folder = _to_local_data_path(year=year, month=month)

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
    return datapath, csvs
