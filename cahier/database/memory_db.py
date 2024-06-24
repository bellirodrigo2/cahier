""" In Memory Database """
from treelib import Tree

################################################################################

tree = Tree()

def get_memory_db():
    """ """
    try:
        yield tree
    finally:
        pass
