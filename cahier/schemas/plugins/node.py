""" Node Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.schemas import BaseNode

###############################################################################


class Node(BaseNode):

    template: str = (Field(),)
