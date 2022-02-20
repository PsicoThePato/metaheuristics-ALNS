from dataclasses import dataclass

from typing import Any


@dataclass
class ProblemDefinition:
    """
    Implements state representation for a given problem
    """
    state: Any
    _file_path: str

    def __init__(self, path: str):
        self.state = None
        self._file_path = path

    def read_from_file(self) -> None:
        """
        Reads state from a file and represents it on object
        """
