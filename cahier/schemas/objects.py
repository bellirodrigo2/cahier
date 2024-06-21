""" Map Objects and hierarchies """
from typing import Annotated
from enum import Enum

from cahier.schemas.base_objects import _BaseObj, _NodeObj, _ItemObj, _ElementObj
from cahier.schemas.loader import load_all_plugins

################################################################################

load_all_plugins()

deriveds = [[c for c in cls.__subclasses__()] for cls in _BaseObj.__subclasses__()]
nested_classes = [item for sublist in deriveds for item in sublist]

parent_map = {x.base_type(): x.parent() for x in nested_classes}
types_map = {x.obj_type(): x.obj_type() for x in nested_classes}
base_map = {x.obj_type(): x.base_type() for x in nested_classes}
init_map = {x.obj_type(): x for x in nested_classes}

class UtilsObjEnum:
    def parent_of(self, child):
        base_child = base_map[child.name]
        base_parent = base_map[self.name]
        possible_parents = parent_map[base_child]
        return base_parent in possible_parents
    
    def make(self, **kwargs):
        return init_map[self.name](**kwargs)

ObjEnum = Enum(
    'ObjEnum',
    types_map,
    module='objects',
    qualname='objects.ObjEnum',
    type=UtilsObjEnum
    )

if __name__ == '__main__':
    
    print('classes ', nested_classes)
    print('parents ', parent_map)
    print('init´s ', init_map)
    print('bases ', base_map)

# from typing import Optional
# from pydantic import BaseModel, Field
# from functools import partial

# FieldDefault = partial(Field, default='NAMEEE')

# namefield = Annotated[str, Field(default='hellow')]

# class model1(BaseModel):
#     name: namefield
#     age: int
    
# class model2(BaseModel):
#     name: namefield | None = None
#     age: int
    
#     # https://stackoverflow.com/questions/67699451/make-every-field-as-optional-with-pydantic
# print(model1(age=23))
# print(model2(age=12).model_dump())