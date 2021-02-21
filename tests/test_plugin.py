from unittest import mock
from pymdmix_core.plugin import PluginManager
from pymdmix_core.parser import get_mdmix_parser, MDMIX_PARSER
from pymdmix_plugin_template.crud_plugin_template import CrudPluginTemplate


def test_plugin_manager_load_plugin_template():
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix_plugin_template")

    assert "plugin_template" in plugin_manager.plugins


@mock.patch("pymdmix_plugin_template.get_plugin_class", return_value=CrudPluginTemplate)
@mock.patch("pymdmix_core.parser.MDMIX_PARSER", get_mdmix_parser())
def test_plugin_manager_load_crud_plugin_template(m_get_plugin_class):
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix_plugin_template")
    assert "crud_plugin_template" in plugin_manager.plugins
    args = MDMIX_PARSER.parse_args(["crud_plugin_template", "list"])
    plugin: CrudPluginTemplate = plugin_manager.plugins["crud_plugin_template"]
    plugin.run(args)
    assert len(plugin.session.query(plugin.CLASS).all()) == 0
