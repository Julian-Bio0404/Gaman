"""Data utils."""

# Utilities
import json


class DotDict(dict):
    """Return dict attributes."""

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def load_data(file: str) -> DotDict:
    """
    Return a dict from json file.
    Param: 
        - file: json file path
    """
    with open(file) as json_file:
        return DotDict(json.load(json_file))
