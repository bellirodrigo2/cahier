""""""

from abc import abstractmethod
from typing import Annotated, Literal, Protocol

from pydantic import BaseModel, Field, field_validator

from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import Obj, WebId

################################################################################


sortOrderLiteral = Literal["Asc", "Desc", "Ascending", "Descending"]


class ReadAllOptions(BaseModel):
    """"""

    field_filter: Annotated[list[str] | None, Field(alias="fieldFilter")] = None
    field_filter_like: Annotated[list[str] | None, Field(alias="fieldFilterLike")] = (
        None
    )
    search_full_hierarchy: Annotated[
        bool | None, Field(alias="searchFullHierarchy")
    ] = None
    sort_field: Annotated[str | None, Field(alias="sortField")] = None
    sort_order: Annotated[sortOrderLiteral | None, Field(alias="sortOrder")] = (
        None  # fazer field validation para tolower()
    )
    start_index: Annotated[int | None, Field(alias="startIndex")] = None
    max_count: Annotated[int | None, Field(alias="maxCount")] = None
    selected_fields: Annotated[list[str] | None, Field(alias="selectedFields")] = None

    @field_validator("sort_order")
    @classmethod
    def tolower(_, name: str) -> str:
        return name.lower()


class RepositoryInterface(Protocol):

    @staticmethod
    @abstractmethod
    def bootstrap(cls) -> None:
        pass

    def get_one_by_webid(self, webid: WebId) -> Obj:
        pass

    def get_all_by_parent_webid(
        self, child: ObjEnum, webid: WebId, query_opt: ReadAllOptions
    ) -> list[Obj]:
        pass

    def add_one(self, webid: WebId, obj: Obj) -> None:
        pass
