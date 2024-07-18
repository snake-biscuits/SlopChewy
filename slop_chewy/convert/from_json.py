from ... import base
from ...sc import SC


def to_sc(jss: base.Binder) -> SC:
    raise NotImplementedError()
    # for each sheet
    # for each block (e.g. A1:C3)
    # create cell

    # auto format
    # column headings line (if row 0 has column names, freeze it)
