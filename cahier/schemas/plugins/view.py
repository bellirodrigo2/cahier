""" View Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.schemas import BaseElement

###############################################################################


class View(BaseElement):

    view_str: str = (Field(),)
