from argparse import ArgumentParser, Namespace
from sqlalchemy import Column, Integer
from pymdmix_core.orm import BaseModel
from pymdmix_core.plugin.crud import CRUDPlugin


class PluginTemplateModel(BaseModel):
    __tablename__ = "plugin_template_models"
    id = Column(Integer(), primary_key=True)


class CrudPluginTemplate(CRUDPlugin):

    NAME = "crud_plugin_template"
    HELP_STRING: str = "crud_plugin_template"
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_crud_plugin_template.yml"
    ALLOW_EMPTY_ACTION = False
    CLASS = PluginTemplateModel

    def __init__(self, master_parser: ArgumentParser) -> None:
        super().__init__(master_parser)

    def init_actions(self, action_subparser):
        return super().init_actions(action_subparser)

    def init_parser(self) -> None:
        return super().init_parser()

    def run(self, args: Namespace) -> None:
        return super().run(args)
