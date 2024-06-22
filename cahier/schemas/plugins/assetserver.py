""" Asset Server Object """

from typing import Annotated

from cahier.schemas.base_objects import ServerObj
from pydantic import AnyUrl, Field

###############################################################################


class AssetServer(ServerObj):

    source_url: Annotated[
        AnyUrl,
        Field(
            alias="SourceURL",
            serialization_alias="SourceURL",
            # default=''
        ),
    ]
