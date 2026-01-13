from fastapi import FastAPI

from routing import modules_injection

def register_middlewares(app: FastAPI) -> None:
    """
    Register middleware for the given FastAPI application.
    """
    # Include the API routes
    for router in modules_injection.routers:
        app.include_router(router)