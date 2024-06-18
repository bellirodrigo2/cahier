""" Cahier Exception """

################################################################################

class CahierException(Exception):
    def __init__(self, message: str = 'Generic Asset Service Error', name: str | None = None) -> None:
        self.message = message
        self.name = name or self.__class__.__name__