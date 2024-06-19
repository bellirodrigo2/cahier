""""""
from typing import Type

from . import ObjEnum, Obj, SingleOutput, ListOutput
from . import Node, Item

################################################################################

#fazer o poprion ObjEnum como Factory

obj_map: dict[ObjEnum, Type[Obj]] = {
    ObjEnum.node: Node,
    ObjEnum.item: Item
}

def cast_obj(tgt_type: ObjEnum, obj: Obj)->Obj:
    return obj_map[tgt_type](**obj)


################################################################################


def make_single_output(obj: Obj)->SingleOutput:
    
    # CRIAR UM MAP DE TYPE PARA LINKS
    # 
    pass

def make_list_output(objs: list[Obj])->ListOutput:
    pass