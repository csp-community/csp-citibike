from functools import lru_cache

import httpx
import pandas as pd

from .urls import (
    CITIBIKE_STATION_INFORMATION,
    CITIBIKE_STATION_STATUS,
    CITIBIKE_VEHICLE_TYPE,
)

__all__ = (
    "get_stations",
    "get_stations_df",
    "get_station_status",
    "get_station_status_df",
    "get_vehicles",
)


@lru_cache
def get_stations():
    dat = httpx.get(CITIBIKE_STATION_INFORMATION).json()
    to_return = {station["station_id"]: station for station in dat["data"]["stations"]}
    # Let's remove the rental uris
    for station in to_return.values():
        station.pop("rental_uris", None)
    return to_return


@lru_cache
def get_stations_df():
    return pd.json_normalize(get_stations().values())


@lru_cache
def get_vehicles():
    dat = httpx.get(CITIBIKE_VEHICLE_TYPE).json()
    return {
        vehicle["vehicle_type_id"]: vehicle for vehicle in dat["data"]["vehicle_types"]
    }


def get_station_status():
    records = httpx.get(CITIBIKE_STATION_STATUS).json()["data"]["stations"]
    stations = get_stations()

    # adjust so that "bikes" means non-ebikes
    for record in records:
        record["total_bikes_available"] = record["num_bikes_available"]
        record["num_bikes_available"] = record["num_bikes_available"] - record.get(
            "num_ebikes_available", 0
        )
        record.pop("vehicle_types_available", None)
        record.update(stations[record["station_id"]])
    return records


def get_station_status_df():
    return pd.json_normalize(get_station_status())
