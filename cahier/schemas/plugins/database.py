""" Database Object """

from typing import Annotated

from pydantic import Field

from cahier.schemas.base_objects import RootObj

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
