""" View Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.base_objects import ElementObj

###############################################################################


class View(ElementObj):

    view_str: Annotated[
        str,
        Field(
            alias="ViewStr",
            serialization_alias="ViewStr",
        ),
    ]
