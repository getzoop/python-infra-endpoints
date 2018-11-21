from .enums import DependencyStatus
from .base import BaseSerialiazable


class Dependency(BaseSerialiazable):

    def __init__(self, name, is_critical, validation_method):
        self._name = name
        self._status = None
        self._isCritical = is_critical
        self._validationMethod = validation_method

        self._exclude_attribute_from_json("validationMethod")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def is_critical(self):
        return self._isCritical

    @is_critical.setter
    def is_critical(self, value):
        self._isCritical = value

    @is_critical.deleter
    def is_critical(self):
        del self._isCritical

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @status.deleter
    def status(self):
        del self._status

    @property
    def validation_method(self):
        return self._validationMethod

    @validation_method.setter
    def validation_method(self, value):
        self._validationMethod = value

    @validation_method.deleter
    def validation_method(self):
        del self._validationMethod

    def execute_validation(self):

        result = self.validation_method()

        if result is True:
            self.status = DependencyStatus.UP
        else:
            self.status = DependencyStatus.DOWN


class AsyncDependency(Dependency):
    def __init__(self, name, is_critical, validation_method):
        super(AsyncDependency, self).__init__(name, is_critical, validation_method)

    async def execute_validation(self):

        result = await self.validation_method()

        if result is True:
            self.status = DependencyStatus.UP
        else:
            self.status = DependencyStatus.DOWN

