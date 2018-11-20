import inspect
from enum import Enum
from http import HTTPStatus

from zpi.common import BaseSerialiazable


class HealthInfrastructure(object):

    def __init__(self):
        self.__health = Health()

    def register_dependency(self, name, is_critical, func, async=False):
        """Add a dependency to dependency list it will be verified to define if application is UP or DOWN"""

        if async is False:
            dep = Dependency(name, is_critical, func)
        else:
            dep = AsyncDependency(name, is_critical, func)

        duplicated = [dep for dep in self.__health.dependencies if str.lower(dep.name) == str.lower(name)]

        if len(duplicated) <= 0:
            self.__health.dependencies.append(dep)

    async def register_async_dependency(self, name, is_critical, func):
        """Add a dependency to dependency list it will be verified to define if application is UP or DOWN"""
        self.register_dependency(name, is_critical, func, True)

    async def check_all_dependencies_status(self):

        async_dependencies = [dependency for dependency in self.__health.dependencies
                              if type(AsyncDependency) is AsyncDependency]

        [await dependency.execute_async_validation() for dependency in async_dependencies]

        self.check_dependencies_status()

    def check_dependencies_status(self):
        """
        Execute verification method in all registered dependencies to define which is UP or DOWN and if
        the application is UP, PARTIAL or DOWN
        """
        sync_dependencies = [dependency for dependency in self.__health.dependencies
                             if type(dependency) is Dependency]

        [dependency.execute_validation() for dependency in sync_dependencies]

        def set_application_status(dependency):

            """Set the application health status based on dependencies status"""

            critical_dependencies = [dep for dep in dependency if dep.is_critical is True]
            non_critical_dependencies = [dep for dep in dependency if dep.is_critical is False]
            application_status = None

            if all((dep.status == DependencyStatus.UP for dep in critical_dependencies)):
                application_status = ApplicationStatus.UP
            elif any((dep.status == DependencyStatus.DOWN for dep in critical_dependencies)) is True:
                application_status = ApplicationStatus.DOWN

            if any((dep.status == DependencyStatus.DOWN for dep in
                    non_critical_dependencies)) is True and application_status == ApplicationStatus.UP:
                application_status = ApplicationStatus.PARTIAL

            return application_status

        self.__health.status = set_application_status(self.__health.dependencies)

    def get_application_health_response(self):
        """Return all health information (application and dependencies) in a json string format"""
        return self.__health.to_json(), self._get_http_code(self.__health.status)

    @staticmethod
    def _get_http_code(status):

        if status == ApplicationStatus.UP:
            return HTTPStatus.OK
        elif status == ApplicationStatus.PARTIAL:
            return HTTPStatus.MULTI_STATUS
        else:
            return HTTPStatus.SERVICE_UNAVAILABLE


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

    # @property
    # def async_dependencies(self):
    #     return self._async_dependencies
    #
    # @async_dependencies.setter
    # def async_dependencies(self, value):
    #     self._async_dependencies = value
    #
    # @async_dependencies.deleter
    # def async_dependencies(self):
    #     del self._async_dependencies


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

        if type(self) is AsyncDependency:
            raise NotImplementedError("Async method not supported. Use 'execute_async_validation' method.")

        result = self.validation_method()

        if result is True:
            self.status = DependencyStatus.UP
        else:
            self.status = DependencyStatus.DOWN

    async def execute_async_validation(self):

        if type(self) is Dependency:
            raise NotImplementedError("Sync method not supported. Use 'execute_validation' method.")

        result = await self.validation_method()

        if result is True:
            self.status = DependencyStatus.UP
        else:
            self.status = DependencyStatus.DOWN


class AsyncDependency(Dependency):
    def __init__(self, name, is_critical, validation_method):
        super(AsyncDependency, self).__init__(name, is_critical, validation_method)


class DependencyStatus(Enum):
    UP = 1
    DOWN = 2

    def __str__(self):
        return str(self.value)


class ApplicationStatus(Enum):
    UP = 1
    PARTIAL = 2
    DOWN = 3

    def __str__(self):
        return str(self.value)
