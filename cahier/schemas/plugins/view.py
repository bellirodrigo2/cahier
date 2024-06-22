""" View Object """

from typing import Annotated

from cahier.schemas.base_objects import ElementObj
from pydantic import Field

###############################################################################


class View(ElementObj):

    view_str: Annotated[
        str,
        Field(
            alias="ViewStr",
            serialization_alias="ViewStr",
        ),
    ]
