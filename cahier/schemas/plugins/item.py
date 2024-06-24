""" Node Object """

from enum import Enum
from typing import Annotated

from pydantic import Field

from cahier.schemas.schemas import BaseItem
from cahier.schemas.timestamp import Timestamp

###############################################################################


class DataTypeEnum(Enum):
    string = str
    float = float
    int = int
    boolean = bool
    byte = bytes
    timestamp = Timestamp


class Item(BaseItem):

    type: DataTypeEnum =Field(),
