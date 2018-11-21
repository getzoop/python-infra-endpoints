
from models.base import BaseSerialiazable
from models.enums import ApplicationStatus


class Health(BaseSerialiazable):

    def __init__(self, dependencies=None):

        if dependencies is None:
            dependencies = list()

        self._status = None
        self._message = None
        self._dependencies = dependencies

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        if value == ApplicationStatus.UP:
            self._message = "All dependencies are up"
        elif value == ApplicationStatus.PARTIAL:
            self._message = "Failure to reach non critical dependencies"
        elif value == ApplicationStatus.DOWN:
            self._message = "Failure to reach critical dependencies"
        else:
            self._message = None

    @status.deleter
    def status(self):
        del self._message

    @property
    def message(self):
        return self._message

    @message.deleter
    def message(self):
        del self._message

    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, value):
        self._dependencies = value

    @dependencies.deleter
    def dependencies(self):
        del self._dependencies
