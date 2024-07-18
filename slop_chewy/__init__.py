__all__ = [
    "base", "convert", "sc",  # modules
    "SC"]  # core classes

# modules
from . import base
from . import convert
# from . import csv
# from . import md
from . import sc
# from . import tsv

# core classes
from .sc import SC  # slop_chewy.SC.from_file(".../somefile.sc")
