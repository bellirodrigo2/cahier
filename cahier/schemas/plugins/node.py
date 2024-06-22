""" Node Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.base_objects import _NodeObj

###############################################################################


class Node(_NodeObj):

    # path: pathField

    template: Annotated[
        str,
        Field(
            alias="Template",
            serialization_alias="Template",
            # default=''
        ),
    ]
