"""Discovery and management for trusted installed NeuralForge plugins."""
from __future__ import annotations
from importlib.metadata import entry_points
from typing import Callable

PLUGIN_GROUP = "neuralforge.plugins"

class PluginManager:
    """Loads plugins installed in the active Python environment.

    Plugins are Python code and therefore have the same permissions as NeuralForge.
    Only install plugins from developers you trust.
    """
    def __init__(self):
        self._plugins = {}

    def discover(self):
        found = entry_points()
        selected = found.select(group=PLUGIN_GROUP) if hasattr(found, "select") else found.get(PLUGIN_GROUP, [])
        for item in selected:
            self._plugins[item.name] = item
        return self.list_plugins()

    def load(self, name):
        if name not in self._plugins:
            self.discover()
        if name not in self._plugins:
            raise KeyError(f"Plugin {name!r} was not found.")
        return self._plugins[name].load()

    def list_plugins(self):
        return [{"name": ep.name, "value": ep.value, "group": PLUGIN_GROUP}
                for ep in self._plugins.values()]
