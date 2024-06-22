""" Node Object """

from enum import Enum
from typing import Annotated

from pydantic import Field

from cahier.schemas.base_objects import _ItemObj
from cahier.schemas.timestamp import Timestamp

###############################################################################


class DataTypeEnum(Enum):
    string = str
    float = float
    int = int
    boolean = bool
    byte = bytes
    timestamp = Timestamp


class Item(_ItemObj):

    # path: pathField

    data_source: Annotated[
        str,
        Field(
            alias="DataSource",
            serialization_alias="DataSource",
        ),
    ]
