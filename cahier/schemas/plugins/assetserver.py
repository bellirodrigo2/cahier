""" Asset Server Object """
from typing import Annotated
from enum import Enum

from pydantic import Field, AnyUrl

from cahier.schemas.base_objects import _ServerObj

################################################################################

class AssetServer(_ServerObj):
    @classmethod
    def obj_type(cls)->str:
        return 'assetserver'
    
    source_url: Annotated[AnyUrl, Field(
        alias='SourceURL',
        serialization_alias='SourceURL',
        # default=''
    )]