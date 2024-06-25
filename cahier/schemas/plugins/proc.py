""" Proc Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.schemas import BaseElement

###############################################################################


class Proc(BaseElement):

    proc_str: str = (Field(),)
