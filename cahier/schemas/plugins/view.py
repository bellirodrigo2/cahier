""" View Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.base_objects import _ElementObj

###############################################################################


class View(_ElementObj):

    view_str: Annotated[
        str,
        Field(
            alias="ViewStr",
            serialization_alias="ViewStr",
        ),
    ]
