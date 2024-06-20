""" Node Object """
from typing import Annotated
from enum import Enum

from pydantic import Field

from cahier.schemas.timestamp import Timestamp
from cahier.schemas.base_objects import _ItemObj

################################################################################

# pathField = Annotated[str, Field(
#         alias='Path',
#         serialization_alias='Path',
#     )]

class DataTypeEnum(Enum):
    string = str
    float = float
    int = int
    boolean = bool
    byte = bytes
    timestamp = Timestamp

class Item(_ItemObj):
    @classmethod
    def obj_type(cls)->str:
        return 'item'
   
    # path: pathField
    
    data_source: Annotated[str, Field(
        alias='DataSource',
        serialization_alias='DataSource',
    )]