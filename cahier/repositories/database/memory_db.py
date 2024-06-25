""" In Memory Database """
from typing import Any, Generator, Callable
from enum import Enum
# from functools import partial
from contextlib import contextmanager

from pydantic import BaseModel
from treelib import Tree

from cahier.schemas.schemas import WebId, ObjEnum, InputObj

################################################################################

def bootstrap(filename: str, **kwargs):
    
    tree = Tree(identifier=filename)

    #inicializa aqui do file json
    
    return tree

@contextmanager
def get_memory_db(tree: Tree)->Generator[Tree, Any, None]:
    """ """
    
    print('here')
    
    try:
        yield tree #PROBLEMA.... tree_session é uma tree aqui e um tree_session no close
    finally:
        tree.save2file(tree.identifier)

if __name__ == '__main__':
    
    tree = bootstrap('hello.json')
    
    db = get_memory_db(tree)
    