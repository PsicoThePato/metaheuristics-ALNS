class ProblemDefinition():
    """
    Implements state representation for a given problem
    """
    def __init__(self):
        self.state = None

    def read_from_file(self, path: str) -> None:
        """
        Reads state from a file and represents it on object
        """
