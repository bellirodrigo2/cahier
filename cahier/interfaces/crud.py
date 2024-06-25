""""""

from enum import Enum
from typing import Any, Protocol

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from cahier.schemas.schemas import InputObj, ObjEnum, WebId

################################################################################


class SortOrder(Enum):
    Asc = "asc"
    Desc = "desc"

class ReadOptions(BaseModel):
    """"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            alias=to_camel, validation_alias=to_camel, serialization_alias=to_camel
        ),
        populate_by_name=True,
        use_enum_values=True,
        frozen=True,
        str_strip_whitespace=True,
        extra="forbid",
    )
    field_filter: list[str] | None = Field(default=None)
    field_filter_like: list[str] | None = Field(default=None)
    search_full_hierarchy: bool | None = Field(default=None)
    sort_field: str | None = Field(default=None)
    sort_order: SortOrder | None = Field(default=None)
    start_index: int | None = Field(default=None)
    max_count: int | None = Field(default=None)
    selected_fields: list[str] | None = Field(default=None)
    
JsonReponse = dict[str, Any]

class CRUDInterface(Protocol):

    def read(self, 
             webid: WebId, target: ObjEnum, options: ReadOptions | None
            ) -> JsonReponse:
        """"""
        pass

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        options: ReadOptions,
    ) -> list[JsonReponse] | JsonReponse:
        """"""
        pass

    def create(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: InputObj
    ) -> WebId:
        """"""
        pass
