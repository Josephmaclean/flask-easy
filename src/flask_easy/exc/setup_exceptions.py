from typing import Optional


class SetupError(Exception):
    description: Optional[str] = None

    def __init__(self, description: Optional[str] = None):
        if description:
            self.description = description


class DBConnectionException(SetupError):
    pass
