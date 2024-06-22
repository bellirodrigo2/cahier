""" Node Object """

from enum import Enum
from typing import Annotated

from cahier.schemas.base_objects import ItemObj
from cahier.schemas.timestamp import Timestamp
from pydantic import Field

###############################################################################


class DataTypeEnum(Enum):
    string = str
    float = float
    int = int
    boolean = bool
    byte = bytes
    timestamp = Timestamp


class Item(ItemObj):

    # path: pathField

    data_source: Annotated[
        str,
        Field(
            alias="DataSource",
            serialization_alias="DataSource",
        ),
    ]
