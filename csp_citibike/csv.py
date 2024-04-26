import csv as pycsv
from datetime import datetime

from csp import ts
from csp.impl.pulladapter import PullInputAdapter
from csp.impl.wiring import py_pull_adapter_def


class CSVAdapterImpl(PullInputAdapter):
    def __init__(self, filename: str, datetime_columns: list = None):
        if not datetime_columns:
            raise Exception("Must provide at least one datetime column")
        self._filename = filename
        self._datetime_columns = datetime_columns
        self._csv_reader = None
        self._first_row = None
        super().__init__()

    def start(self, starttime, endtime):
        super().start(starttime, endtime)
        self._csv_reader = pycsv.DictReader(open(self._filename, "r"))

        # fast forward to first record
        while True:
            try:
                row = next(self._csv_reader)
                time = datetime.strptime(
                    row[self._datetime_columns[0]], "%Y-%m-%d %H:%M:%S"
                )

                if time < starttime:
                    continue

                for dtc in self._datetime_columns:
                    row[dtc] = datetime.strptime(row[dtc], "%Y-%m-%d %H:%M:%S")
                self._first_row = row
                break

            except StopIteration:
                return

    def stop(self):
        self._csv_reader = None

    def next(self):
        if self._first_row is not None:
            ret = self._first_row[self._datetime_columns[0]], self._first_row
            self._first_row = None
        try:
            row = next(self._csv_reader)
            time = datetime.strptime(
                row[self._datetime_columns[0]], "%Y-%m-%d %H:%M:%S"
            )
            for dtc in self._datetime_columns:
                row[dtc] = datetime.strptime(row[dtc], "%Y-%m-%d %H:%M:%S")
            return time, row
        except StopIteration:
            return None


CSVAdapter = py_pull_adapter_def(
    "CSVAdapter", CSVAdapterImpl, ts[dict], filename=str, datetime_columns=list
)
