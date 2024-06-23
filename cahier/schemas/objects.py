""" Map Objects and hierarchies """

import os
from typing import Annotated, Type
from enum import Enum

from pydantic import BaseModel, Field, field_validator, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel

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
        extra='allow'
    )

    field_filter: Annotated[list[str] | None, Field()] = None
    field_filter_like: Annotated[list[str] | None, Field()] = None
    search_full_hierarchy: Annotated[bool | None, Field()] = None
    sort_field: Annotated[str | None, Field()] = None
    sort_order: Annotated[SortOrder | None, Field()] = None
    start_index: Annotated[int | None, Field()] = None
    max_count: Annotated[int | None, Field()] = None
    selected_fields: Annotated[list[str] | None, Field()] = None

if __name__ == "__main__":
    pass
    # print('classes ', nested_classes)
    # print('parents ', parent_map)
    # print('init´s ', init_map)
    # print('bases ', base_map)
