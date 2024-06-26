""" Container """
from typing import Callable
from functools import partial

################################################################################

container = {}
dep_configs = {}

def inject_dependency(key: str, dep: Callable, **configs)->None:
    
    if key in container:
        raise Exception()

    container[key] = dep
    dep_configs[key] = configs
    
def provide_dependency(key: str, **override_configs)->Callable:
    
    if key not in container:
        raise Exception()
    
    merged_config = {**dep_configs[key], **override_configs}
    return partial(container[key], **merged_config)

def inspect_dependencies()->list[str]:
    return container.keys()

if __name__ == '__main__':
    
    def get_dep1(name: str, url:str, level:int):
        return f'{name}/{url}/{level}'
    
    inject_dependency('dep1', dep= get_dep1, name='RBELLI', url='cahier.com', level=10)
    
    depa = provide_dependency('dep1')
    print(depa())
    
    depb = provide_dependency('dep1', name='NAMe2', url='NEWURL.com', level=45)
    print(depb())
    
    try:
        depc = provide_dependency('dep1', NOKEY='NAMe2', url='NEWURL.com', level=45)
        print(depc())
    except Exception as e:
        print(e)