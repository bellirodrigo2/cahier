""""""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .routers.asset import router as asset_router

################################################################################

def create_api(routers: list, container: dict):
    
    #como injetar handlers ???
    #https://python-dependency-injector.ets-labs.org/examples/fastapi.html

    container.config.giphy.api_key.from_env("GIPHY_API_KEY")

    app = FastAPI()
    # from dependency_injector.wiring import inject, Provide
    app.container = container

    # app.include_router(asset_router)
    for router in routers:
        app.include_router(router)

    @app.exception_handler(HTTPException)
    async def handle_invalid_request(request, exc):
        print("********************", exc)
        return JSONResponse(status_code=300, content=str(exc))

    return app