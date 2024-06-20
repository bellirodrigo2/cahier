""" Database Object """
from typing import Annotated
from enum import Enum

from pydantic import Field

from cahier.schemas.base_objects import _RootObj

################################################################################

class DataBase(_RootObj):
    @classmethod
    def obj_type(cls)->str:
        return 'database'
    
    db_field: Annotated[str, Field(
        alias='DBField',
        serialization_alias='DBField',
        # default=''
    )]