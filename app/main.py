# -*- coding: utf-8 -*-
from starlette.applications import Starlette
from starlette.routing import Mount, Route, Router
from resources import init_app
import settings
from app_functions import exceptions
import resources
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from endpoints.main import endpoints as main_pages
from endpoints.health import endpoints as health_pages
from endpoints.pages import endpoints as pages
from starlette.staticfiles import StaticFiles
import httpx

routes = [
    Route("/", main_pages.homepage, name="dashboard", methods=["GET"]),
    Mount(
        "/health",
        routes=[
            Route("/status", endpoint=health_pages.health_status, methods=["GET"]),
        ],
        name="health",
    ),
    Mount(
        "/pages",
        routes=[
            Route("/{page}", endpoint=pages.example_pages, methods=["GET"]),
            Route(
                "/charts/{page}", endpoint=pages.example_pages_charts, methods=["GET"]
            ),
            Route(
                "/examples/{page}",
                endpoint=pages.example_pages_examples,
                methods=["GET"],
            ),
            Route("/forms/{page}", endpoint=pages.example_pages_forms, methods=["GET"]),
            Route(
                "/mailbox/{page}", endpoint=pages.example_pages_mailbox, methods=["GET"]
            ),
            Route(
                "/data_tables/{page}",
                endpoint=pages.example_pages_tables,
                methods=["GET"],
            ),
            Route("/ui/{page}", endpoint=pages.example_pages_ui, methods=["GET"]),
        ],
        name="pages",
    ),
    Mount("/static", app=StaticFiles(directory="statics"), name="static"),
    # Mount("/static", statics, name="static"),
    # Mount("/user", routes=user_routes, name='user'),
    # WebSocketRoute("/ws", websocket_endpoint),
]



middleware = [Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)]

exception_handlers = {
    403: exceptions.not_allowed,
    404: exceptions.not_found,
    500: exceptions.server_error,
}

init_app()

app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    on_startup=[resources.startup],
    on_shutdown=[resources.shutdown],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info", debug=settings.DEBUG)
