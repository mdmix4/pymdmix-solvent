from argparse import ArgumentParser, Namespace
from pymdmix_core.plugin.base import Plugin


class PluginTemplate(Plugin):

    NAME = "plugin_template"
    HELP_STRING: str = "plugin_template"
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_plugin_template.yml"
    ALLOW_EMPTY_ACTION = False

    def __init__(self, master_parser: ArgumentParser) -> None:
        super().__init__(master_parser)

    def init_actions(self, action_subparser):
        return super().init_actions(action_subparser)

    def init_parser(self) -> None:
        return super().init_parser()

    def run(self, args: Namespace) -> None:
        return super().run(args)
