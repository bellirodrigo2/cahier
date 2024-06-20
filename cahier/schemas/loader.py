
"""A simple plugin loader."""
import importlib
import os

################################################################################

def import_module(name: str):
    """Imports a module given a name."""
    return importlib.import_module(f'{__package__}.{name}')


def get_plugins(path: str)->list[str]:
    """Get the python files from parent 'plugin' folder."""
    
    walk_list:list[str] = list(
        next(os.walk(f'{path}/plugins'), (None, None, []))[2]
        )
    
    return [f'plugins.{x}'.replace('.py','') 
            for x in walk_list 
                if x.endswith('.py') and x.startswith('__init__') == False]

def load_all_plugins() -> None:
    """Loads the plugins defined in the plugins list."""
    
    plugins = get_plugins(os.path.dirname(__file__))
    for plugin_file in plugins:
        plugin = import_module(plugin_file)