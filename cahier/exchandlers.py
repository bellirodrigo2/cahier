""" Exceptions Handlers """
from typing import Callable

from fastapi import status, Request
from fastapi.responses import JSONResponse

from .exceptions import CahierException

################################################################################

def create_exception_handler(
    status_code: int, initial_detail: str,
)-> Callable[[Request, CahierException], JSONResponse]:
    
    detail = {'message': initial_detail}
    
    def exception_handler(_: Request, exc: CahierException)-> JSONResponse:
        
        if exc.message:
            detail['message'] = exc.message

        if exc.name:
            detail['message'] = f'{detail['message']} [{exc.name}]'
        
        return JSONResponse(
            status_code=status_code, content={'detail': detail['message']}
        )
        
    return exception_handler