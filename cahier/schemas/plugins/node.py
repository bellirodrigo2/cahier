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
    
    # path: pathField
    
    template: Annotated[str, Field(
        alias='Template',
        serialization_alias='Template',
        # default=''
    )]