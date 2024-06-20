""" View Object """
from typing import Annotated

from pydantic import Field

from cahier.schemas.base_objects import _ElementObj

################################################################################

class View(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'view'
    
    view_str: Annotated[str, Field(
        alias='ViewStr',
        serialization_alias='ViewStr',
    )]
    