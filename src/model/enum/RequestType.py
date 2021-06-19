from enum import Enum, auto


class AccountType(Enum):
    def __str__(self):
        return str(self.name)

    NONR = auto()
    RRSP = auto()
    TFSA = auto()
