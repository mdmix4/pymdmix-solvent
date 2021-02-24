from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import os
import sqlalchemy

from unittest.mock import patch


FPATH = os.path.join("tests", "fixtures")


@contextmanager
def db_patch():
    try:
        tmpfile = NamedTemporaryFile()
        with patch(
            "pymdmix_core.plugin.crud.SQL_ENGINE",
            sqlalchemy.create_engine(f"sqlite:///{tmpfile.name}")
        ) as db_engine:
            yield db_engine
    finally:
        tmpfile.close()
