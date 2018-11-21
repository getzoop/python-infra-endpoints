import sys

from models.base import BaseSerialiazable


class ApplicationInfo(BaseSerialiazable):

    def __init__(self):
        self._build_number = None
        self._application_name = None
        self._created_by = None
        self._version = None
        self._python_version = sys.version.replace("\n", '')

    @property
    def application_name(self):
        return self._application_name

    @application_name.setter
    def application_name(self, app_name):
        self._application_name = app_name

    @application_name.deleter
    def application_name(self):
        del self._application_name

    @property
    def created_by(self):
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        self._created_by = created_by

    @created_by.deleter
    def created_by(self):
        del self._created_by

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @version.deleter
    def version(self):
        del self._version

    @property
    def build_number(self):
        return self._build_number

    @build_number.setter
    def build_number(self, build_number):
        self._build_number = build_number

    @build_number.deleter
    def build_number(self):
        del self._build_number

    @property
    def python_version(self):
        return self._python_version

    @python_version.deleter
    def python_version(self):
        del self._python_version
