""""""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .routers.asset import router as asset_router

# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from .exceptions import AssetTypeHierarchyError, type_hierarchy_handler
# from .exceptions import InconsistentAssetTypeError, inconsistent_type_handler

################################################################################

app = FastAPI()

app.include_router(asset_router)

# class PrintMiddleware(BaseHTTPMiddleware):
# async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
# ic(request.method, request.url.path, request.url.query)

# resp = await call_next(request)
# return resp

# app.add_middleware(PrintMiddleware)


# async def my_middleware(request: Request, call_next: Callable, some_attribute: Any) -> Response:
# request.state.attr = some_attribute  # Do what you need with your attribute
# return await call_next(request)

# my_custom_middleware: partial[Coroutine[Any, Any, Any]] = partial(my_middleware, some_attribute="my-app")

# app.middleware("http")(my_custom_middlware)

# def my_http_exception_handler(request: Request, exc: HTTPException):
# return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
# app.add_exception_handler(MyHTTPException, my_http_exception_handler)


@app.exception_handler(HTTPException)
async def handle_invalid_request(request, exc):
    print("********************", exc)
    return JSONResponse(status_code=300, content=str(exc))


# app.add_exception_handler(
# exc_class_or_status_code=InconsistentAssetTypeError,
# handler=inconsistent_type_handler
# )
