import sqlite3

from ..sc import SC
from .common import JsonSpreadSheet


def to_json(sql_db: sqlite3.Connection) -> JsonSpreadSheet:
    raise NotImplementedError()
    # get all table names
    # get per-table column names
    # get per-row types (useful for formatting)

    # one sheet per table
    # top row is column names (frozen)
    # order by rowid


def to_sc(sql_db: sqlite3.Connection, include_views=True) -> SC:
    raise NotImplementedError()
    # TODO: wrap ..from_json.to_sc
