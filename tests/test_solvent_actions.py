import os
import shlex
import sqlalchemy
from pymdmix_core.plugin import PluginManager
from pymdmix_core.parser import get_mdmix_parser
from pymdmix_solvent.solvent import Probe, ProbeType, Solvent
from .conftest import FPATH
from unittest.mock import patch
# TODO:
# test solvent creation, single solvent per file
# test solvent creation, multiple solvents per file
# test solvent deletion.
#   it should delete the solvent and probes, but not the probe_types
# test grouping by probe
# test grouping by probe type


def get_plugin_manager() -> PluginManager:
    plugin_manager = PluginManager(get_mdmix_parser())
    plugin_manager.load_plugin("pymdmix_solvent")
    return plugin_manager


def run_command(cmd: str, plugin_manager = None):
    plugin_manager = plugin_manager if plugin_manager is not None else get_plugin_manager()
    args = plugin_manager.parser.parse_args(shlex.split(cmd))
    plugin_manager.plugins["solvent"].run(args)


def test_solvent_creation(tmpdir):
    config_file = os.path.join(FPATH, "iso5.yml")
    with patch("pymdmix_core.plugin.crud.SQL_ENGINE", sqlalchemy.create_engine(f"sqlite:///{tmpdir}/test.db")):
        plugin_manager = get_plugin_manager()
        run_command(f"solvent create --yaml {config_file}", plugin_manager)
        session = plugin_manager.plugins["solvent"].session
        assert len(session.query(Solvent).all()) == 1
        assert len(session.query(Probe).all()) == 3
        assert len(session.query(ProbeType).all()) == 4

        run_command("solvent delete ISO5")
        assert len(session.query(Solvent).all()) == 0
        assert len(session.query(Probe).all()) == 0
        assert len(session.query(ProbeType).all()) == 4
