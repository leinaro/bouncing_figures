from enum import Enum


class CInputCommand:
    def __init__(self, name: str, key: str):
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA

class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2