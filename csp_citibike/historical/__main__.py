import sys

from .download import download_data


def main():
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
            month = int(sys.argv[2])
        except Exception:
            print("Usage: python -m csp_citibike.data <year> <month>")
            return
    else:
        year = None
        month = None
    download_data(year=year, month=month)


if __name__ == "__main__":
    main()
