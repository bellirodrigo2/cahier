""" Asset Server Object """

from pydantic import AnyUrl, Field

from cahier.schemas.schemas import BaseServer

###############################################################################


class AssetServer(BaseServer):
    source_url: AnyUrl = (Field(),)
