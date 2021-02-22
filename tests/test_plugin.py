from tests.conftest import db_patch
from unittest import mock
from pymdmix_core.plugin import PluginManager
from pymdmix_core.parser import get_mdmix_parser, MDMIX_PARSER
from pymdmix_solvent.solvent import SolventPlugin


@db_patch()
def test_plugin_manager_load_solvent():
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix_solvent")
    assert "solvent" in plugin_manager.plugins


@db_patch()
@mock.patch("pymdmix_solvent.get_plugin_class", return_value=SolventPlugin)
@mock.patch("pymdmix_core.parser.MDMIX_PARSER", get_mdmix_parser())
def test_plugin_manager_load_crud_solvent(m_get_plugin_class):
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix_solvent")
    assert "solvent" in plugin_manager.plugins
    args = MDMIX_PARSER.parse_args(["solvent", "list"])
    plugin: SolventPlugin = plugin_manager.plugins["solvent"]
    plugin.run(args)
    assert len(plugin.session.query(plugin.CLASS).all()) == 0
