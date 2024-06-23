""" Asset Server Object """

from typing import Annotated

from pydantic import AnyUrl, Field

from cahier.schemas.base_objects import ServerObj

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
