""""""
from typing import Callable
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from cahier.container import inject_dependency
from cahier.interfaces.assetservice import AssetInterface
from cahier.interfaces.assetdao import AssetDAOInterface

################################################################################

def create_api(
    routers: list, 
    get_asset_service: Callable[..., AssetInterface],
    asset_service_configs: dict,
    get_asset_dao: Callable[..., AssetDAOInterface],
    asset_dao_configs: dict,
    ):
    
    inject_dependency(key='asset_service', dep=get_asset_service, **asset_service_configs)
    inject_dependency(key='asset_dao', dep=get_asset_dao, **asset_dao_configs)

    app = FastAPI()
    for router in routers:
        app.include_router(router)

    @app.exception_handler(HTTPException)
    async def handle_invalid_request(request, exc):
        return JSONResponse(status_code=300, content=str(exc))

    return app