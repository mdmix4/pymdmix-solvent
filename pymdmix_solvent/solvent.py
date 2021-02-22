import os
from argparse import ArgumentParser, Namespace
from sqlalchemy import Column, String, LargeBinary
from pymdmix_core.orm import BaseModel
from pymdmix_core.plugin.crud import ActionDelete, CRUDPlugin, parse_file_from_args
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table


class ActionDeleteSolvent(ActionDelete):

    def run(self, args: Namespace) -> None:
        session = self.parent_plugin.session
        model_class = self.parent_plugin.CLASS
        query = session.query(model_class).filter(model_class.id.in_(args.id))
        for model in query.all():
            session.delete(model)
        session.commit()


PROBES_TO_TYPES_ASSOCIATION_TABLE = Table(
    'probes_to_types_association',
    BaseModel.metadata,
    Column('probe_id', String, ForeignKey("solvent_probes.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column('probe_type_id', String, ForeignKey("solvent_probe_types.id"))
)


class Solvent(BaseModel):
    __tablename__ = "solvents"
    id = Column(String, primary_key=True)
    info = Column(String)
    unit = Column(String)
    off_file = Column(LargeBinary)
    probes = relationship("Probe", cascade="all, delete, delete-orphan")


class Probe(BaseModel):
    __tablename__ = "solvent_probes"
    
    id = Column(String, primary_key=True)
    solvent = Column(
        String,
        ForeignKey(
            "solvents.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        primary_key=True,
        nullable=False
    )
    mask = Column(String)
    types = relationship("ProbeType", secondary=PROBES_TO_TYPES_ASSOCIATION_TABLE)
    

class ProbeType(BaseModel):
    __tablename__ = "solvent_probe_types"
    id = Column(String, primary_key=True)


class SolventPlugin(CRUDPlugin):

    NAME = "solvent"
    HELP_STRING: str = ""
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_solvent.yml"
    ALLOW_EMPTY_ACTION = False
    CLASS = Solvent

    def __init__(self, master_parser: ArgumentParser) -> None:
        super().__init__(master_parser)

    def init_actions(self, action_subparser):
        super().init_actions(action_subparser)
        self.register_action(ActionDeleteSolvent(action_subparser, self))

    def init_parser(self) -> None:
        return super().init_parser()

    def run(self, args: Namespace) -> None:
        return super().run(args)

    def factory(self, args: Namespace) -> Solvent:
        fields = parse_file_from_args(args)
        if fields is None:
            raise ValueError("unable to read config file for solvent")
        config_file = args.json if args.json is not None else args.yaml
        models = []
        for solvent_id, values in fields.items():
            off_file = values["off_file"]
            if not os.path.exists(off_file):
                base_path = os.path.dirname(config_file)
                off_file = os.path.join(base_path, off_file)

            off_file_data = None
            with open(off_file, 'rb') as file:
                off_file_data = file.read()

            solvent_data = {
                "id": solvent_id,
                "info": values.get("info"),
                "off_file": off_file_data,
                "unit": values.get("unit"),
            }
            solvent = Solvent(**solvent_data)
            self.session.add(solvent)

            for probe_id, probe_fields in values.get("probes", {}).items():
                probe_data = {
                    "id": probe_id,
                    "solvent": solvent.id,
                    "mask": probe_fields.get("mask"),
                }
                probe = Probe(**probe_data)
                self.session.add(probe)
                for probe_type in probe_fields.get("types", []):
                    current = self.session.query(ProbeType).filter(ProbeType.id == probe_type).first()
                    if current is None:
                        current = ProbeType(id=probe_type)
                        self.session.add(current)
                    probe.types.append(current)
                solvent.probes.append(probe)
            self.session.commit()
            models.append(solvent)
        return models if len(models) > 0 else None
