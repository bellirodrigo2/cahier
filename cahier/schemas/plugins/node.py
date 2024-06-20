""" Node Object """
from typing import Annotated
from enum import Enum

from pydantic import Field

from cahier.schemas.base_objects import _NodeObj

################################################################################

# pathField = Annotated[str, Field(
#         alias='Path',
#         serialization_alias='Path',
#     )]

class Node(_NodeObj):
    @classmethod
    def obj_type(cls)->str:
        return 'node'
    
    # path: pathField
    
    template: Annotated[str, Field(
        alias='Template',
        serialization_alias='Template',
        # default=''
    )]