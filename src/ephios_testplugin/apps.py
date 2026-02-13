from ephios.core.plugins import PluginConfig


class PluginApp(PluginConfig):
    name = "ephios_testplugin"

    class EphiosPluginMeta:
        name = "Ephios Test Plugin"
        author = "Felix Rindt"
        description = "A test plugin for ephios"

    def ready(self):
        from . import signals  # NOQA
