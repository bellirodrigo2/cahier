""" Database Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.schemas import BaseRoot

###############################################################################


class DataBase(BaseRoot):

    host: str = (Field(),)
