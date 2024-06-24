""""""
from typing import Any, Protocol
from enum import Enum

from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel

from cahier.schemas.schemas import ObjEnum, WebId
from cahier.schemas.schemas import BaseOutput, ListOutput, BaseInputObj

################################################################################

class SortOrder(Enum):
    Asc = 'asc'
    Desc = 'desc'

class ReadAllOptions(BaseModel):
    """"""
    model_config = ConfigDict(
                alias_generator=AliasGenerator(
                    alias=to_camel,
                    validation_alias=to_camel,
                    serialization_alias=to_camel
                ),
                populate_by_name=True,
                use_enum_values=True,
                frozen=True,
                str_strip_whitespace=True,
                extra='forbid'
            )


    field_filter: list[str] | None = Field(default=None)
    field_filter_like: list[str] | None = Field(default=None)
    search_full_hierarchy: bool | None = Field(default=None)
    sort_field: str | None = Field(default=None)
    sort_order: SortOrder | None = Field(default=None)
    start_index: int | None = Field(default=None)
    max_count: int | None = Field(default=None)
    selected_fields: list[str] | None = Field(default=None)

class CRUDInterface(Protocol):

    def read(self, webid: WebId, target_type: ObjEnum) -> BaseOutput:
        """"""
        pass

    def list(self, parent: ObjEnum, children: ObjEnum, webid: WebId, 
            query_dict: ReadAllOptions) -> list[BaseOutput] | ListOutput:
        """"""
        pass

    def create(self, parent: ObjEnum, children: ObjEnum, webid: WebId, 
               obj: BaseInputObj) -> None:
        """"""
        pass
