""" Container """
from typing import Callable
from functools import partial

################################################################################

container = {}
configs = {}

def inject(key: str, dep: Callable, **configs):
    
    if key in container:
        raise Exception()
    
    container[key] = dep
    configs[key] = configs
    
def provide(key: str, **override_configs):
    
    if key not in container:
        raise Exception()
    
    merged_config = {**configs[key], **override_configs}
    return partial(container[key], merged_config)