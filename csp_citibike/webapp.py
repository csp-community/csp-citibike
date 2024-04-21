# import asyncio
# import logging
# import threading
# import uvicorn
# from fastapi import FastAPI
# from perspective import Table, PerspectiveManager, PerspectiveStarletteHandler

# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.staticfiles import StaticFiles

# __all__ = (
#   "make_perspective_app",
#   "run_csp_citibike",
#   "main",
# )


# def make_perspective_app(app: FastAPI, manager: PerspectiveManager):
#     '''Code to create a Perspective webserver. This code is adapted from
#     https://github.com/finos/perspective/blob/master/examples/python-starlette/server.py

#     Args:
#         app (FastAPI): FastAPI Application
#         manager (PerspectiveManager): PerspectiveManager instance (hosts the tables)

#     Returns:
#         app: returns the FastAPI back
#     '''
#     def perspective_thread(manager):
#         # This thread runs the perspective processing callback
#         psp_loop = asyncio.new_event_loop()
#         manager.set_loop_callback(psp_loop.call_soon_threadsafe)
#         psp_loop.run_forever()

#     thread = threading.Thread(target=perspective_thread, args=(manager,), daemon=True)
#     thread.start()

#     async def websocket_handler(websocket: WebSocket):
#         handler = PerspectiveStarletteHandler(manager=manager, websocket=websocket)
#         await handler.run()

#     app = FastAPI()
#     app.add_api_websocket_route("/websocket", websocket_handler)
#     app.mount("/", StaticFiles(directory="static", html=True))

#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#     return app


# def run_csp_citibike(manager: PerspectiveManager):
#     '''Connect to csp to perspective and load data

#     Args:
#         manager (PerspectiveManager): PerspectiveManager instance (hosts the tables)
#     '''
#     raise NotImplementedError()


# def main():
#     app = FastAPI()
#     perspective_manager = PerspectiveManager()

#     make_perspective_app(app, perspective_manager)
#     run_csp_citibike(perspective_manager)
#     logging.critical("Listening on http://localhost:8080")
#     uvicorn.run(app, host="0.0.0.0", port=8080)
