import asyncio
import logging
import os.path
import threading
from datetime import datetime, timedelta

import csp
import uvicorn
from csp import ts
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from perspective import PerspectiveManager, PerspectiveStarletteHandler
from perspective import Table as PerspectiveTable
from starlette.staticfiles import StaticFiles

from csp_citibike import get_station_status


def make_perspective_app(manager: PerspectiveManager):
    """Code to create a Perspective webserver. This code is adapted from
    https://github.com/finos/perspective/blob/master/examples/python-starlette/server.py

    Args:
        manager (PerspectiveManager): PerspectiveManager instance (hosts the tables)

    Returns:
        app: returns the FastAPI back
    """

    def perspective_thread(manager):
        # This thread runs the perspective processing callback
        psp_loop = asyncio.new_event_loop()
        manager.set_loop_callback(psp_loop.call_soon_threadsafe)
        psp_loop.run_forever()

    thread = threading.Thread(target=perspective_thread, args=(manager,), daemon=True)
    thread.start()

    async def websocket_handler(websocket: WebSocket):
        handler = PerspectiveStarletteHandler(manager=manager, websocket=websocket)
        try:
            await handler.run()
        except Exception:
            ...

    app = FastAPI()
    app.add_api_websocket_route("/websocket", websocket_handler)
    app.mount(
        "/",
        StaticFiles(
            directory=os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "static"
            ),
            html=True,
        ),
        name="static",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


@csp.node
def push_to_perspective_table(data: ts[list], table: PerspectiveTable):
    if csp.ticked(data):
        table.update(data)


@csp.node
def poll_data(interval: timedelta) -> ts[[dict]]:
    with csp.alarms():
        # this line tells `csp` we will have an alarm
        # we will schedule the alarm in a later step
        a_poll = csp.alarm(bool)

    with csp.start():
        # poll immediately after starting
        # by passing timedelta(seconds=0)
        csp.schedule_alarm(a_poll, timedelta(), True)

    if csp.ticked(a_poll):
        # grab the data
        to_return = get_station_status()

        # schedule next poll in `interval`
        csp.schedule_alarm(a_poll, interval, True)
        return to_return


@csp.graph
def main_graph(table: PerspectiveTable, interval: timedelta = timedelta(seconds=60)):
    # push all of our data to 4 separate perspective tables
    data = poll_data(interval)
    push_to_perspective_table(data, table)


def run_csp(manager: PerspectiveManager):
    """Connect to csp to perspective and load data

    Args:
        manager (PerspectiveManager): PerspectiveManager instance (hosts the tables)
    """
    table = PerspectiveTable(
        {
            "station_id": str,
            "lat": float,
            "capacity": int,
            "lon": float,
            "name": str,
            "num_scooters_available": int,
            "num_scooters_unavailable": int,
            "num_docks_disabled": int,
            "last_reported": datetime,
            "num_bikes_disabled": int,
            "is_renting": bool,
            "is_returning": bool,
            "num_docks_available": int,
            "is_installed": bool,
            "num_ebikes_available": int,
            "num_bikes_available": int,
            "total_bikes_available": int,
        },
        index="station_id",
    )

    # host these tables
    manager.host_table("data", table)

    # run csp
    logging.critical("running csp...")
    return csp.run_on_thread(main_graph, table, realtime=True, daemon=True)


def main():
    perspective_manager = PerspectiveManager()

    app = make_perspective_app(perspective_manager)
    run_csp(perspective_manager)
    logging.critical("Listening on http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
