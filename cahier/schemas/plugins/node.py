""" Node Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.schemas import NodeObj

###############################################################################


class Node(NodeObj):

    template: str = Field(),
