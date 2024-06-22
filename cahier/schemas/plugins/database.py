""" Database Object """

from typing import Annotated

from cahier.schemas.base_objects import RootObj
from pydantic import Field

###############################################################################


class DataBase(RootObj):

    db_field: Annotated[
        str,
        Field(
            alias="DBField",
            serialization_alias="DBField",
            # default=''
        ),
    ]
