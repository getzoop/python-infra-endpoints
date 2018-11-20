from enum import IntEnum


class DependencyStatus(IntEnum):
    UP = 1
    DOWN = 2

    def __str__(self):
        return str(self.value)


class ApplicationStatus(IntEnum):
    UP = 1
    PARTIAL = 2
    DOWN = 3

    def __str__(self):
        return str(self.value)
