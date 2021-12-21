class BaseState():
    """
    Implements state representation for a given problem
    """
    def __init__(self):
        self.state = None

    def read_from_file(self, path: str) -> None:
        """
        Reads state from a file and represents it on object
        """

class BaseMethods():
    """
    Implements destroy and repair methods to be used on ALNS.
    """
    def __init__(self):
        self.destroy_heuristics = []
        self.repair_heuristics = []
        self._set_heuristics()

    def destroy(self, destruction_parameter: float, state: BaseState) -> BaseState:
        """
        Selects a destroy heuristic at random, use it to deconstruct given state
        and returns an incomplete state
        """

    def repair(self, state: BaseState) -> BaseState:
        """
        Selects a repair heuristic at random, use it to reconstruct an incomplete
        state and returns the new state
        """

    def _set_heuristics(self) -> None:
        """
        adds destroy and repair heuristics to class object
        """


class ALNS():
    """
    ALNS metaheuristic implementation
    """
    def __init__(self, state: BaseState, methods: BaseMethods):
        self.state = state
        self.methods = methods

    # TODO the remainder of the class :<
    # TODO move it to meta folder
