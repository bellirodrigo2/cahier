""""""

from fastapi import FastAPI

from .routers.asset import router as asset_router
from .exceptions import AssetTypeHierarchyError, type_hierarchy_handler
from .exceptions import InconsistentAssetTypeError, inconsistent_type_handler

################################################################################

app = FastAPI()

app.include_router(asset_router)

app.add_exception_handler(
    exc_class_or_status_code=AssetTypeHierarchyError,
    handler=type_hierarchy_handler
    )

app.add_exception_handler(
    exc_class_or_status_code=InconsistentAssetTypeError,
    handler=inconsistent_type_handler
    )