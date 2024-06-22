""" Node Object """

from typing import Annotated

from cahier.schemas.base_objects import NodeObj
from pydantic import Field

###############################################################################


class Node(NodeObj):

    # path: pathField

    template: Annotated[
        str,
        Field(
            alias="Template",
            serialization_alias="Template",
            # default=''
        ),
    ]
