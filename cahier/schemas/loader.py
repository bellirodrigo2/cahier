"""A simple plugin loader."""

import importlib
import os

###############################################################################


def import_module(name: str):
    """Imports a module given a name."""
    return importlib.import_module(f"{__package__}.{name}")


TARGET_FOLDER = "plugins"


def file_to_module_name(file: str) -> str:
    return f"{TARGET_FOLDER}.{file}".replace(".py", "")


def read_all_files(path: str) -> list[str]:
    return list(next(os.walk(f"{path}/{TARGET_FOLDER}"), (None, None, []))[2])


def get_plugins(path: str) -> list[str]:
    """Get the python files from parent 'plugin' folder."""

    walk_list: list[str] = read_all_files(path)

    return [
        file_to_module_name(x)
        for x in walk_list
        if x.endswith(".py") and x.startswith("__init__") is False
    ]


def load_all_plugins() -> None:
    """Loads the plugins defined in the plugins list."""

    plugins = get_plugins(os.path.dirname(__file__))
    assert len(plugins) > 0, "No Plugins loaded"
    for plugin_file in plugins:
        import_module(plugin_file)
