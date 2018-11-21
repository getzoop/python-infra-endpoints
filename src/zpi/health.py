from http import HTTPStatus

from zpi.models.health import Health
from zpi.models.dependency import AsyncDependency, Dependency
from zpi.models.enums import DependencyStatus, ApplicationStatus


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
