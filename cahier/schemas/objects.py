""" Map Objects and hierarchies """

import os
from typing import Annotated, Type
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from cahier.schemas.base_objects import BaseObj
from cahier.schemas.loader import load_all_plugins
from cahier.schemas.makeenums import make_enum, name, EnumBase

###############################################################################

load_all_plugins(os.path.dirname(__file__), "plugins")


class UtilsObjEnum(EnumBase):

    @classmethod
    def init_class(cls, classes_list: list[BaseObj]):
        cls.__base_map = {name(x): x.base_type() for x in classes_list}
        cls.__parent_map = {x.base_type(): x.parent() for x in classes_list}
        super().init_class(classes_list)

    def parent_of(self, child):
        cls = self.__class__
        base_child = cls.__base_map[child.name]
        base_parent = cls.__base_map[self.name]
        possible_parents = cls.__parent_map[base_child]
        return base_parent in possible_parents

    def children_of(self, child):
        pass

# ESSE TYPE HINT TEM QUE FUNCIONAR
ObjEnum: Type[UtilsObjEnum] = make_enum(base_class=BaseObj, enum_base=UtilsObjEnum)


class SortOrder(Enum):
    Asc = 'Asc'
    Desc = 'Desc'

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
    sort_order: Annotated[SortOrder | None, Field(alias="sortOrder")] = (
        None  # fazer field validation para tolower()
    )
    start_index: Annotated[int | None, Field(alias="startIndex")] = None
    max_count: Annotated[int | None, Field(alias="maxCount")] = None
    selected_fields: Annotated[list[str] | None, Field(alias="selectedFields")] = None

    @field_validator("sort_order")
    @classmethod
    def tolower(cls, name: str) -> str:
        return name.lower()


if __name__ == "__main__":
    pass
    # print('classes ', nested_classes)
    # print('parents ', parent_map)
    # print('init´s ', init_map)
    # print('bases ', base_map)
