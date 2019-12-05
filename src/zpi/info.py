import os

import yaml

from zpi.models.application_info import ApplicationInfo


class InfoInfrastructure(object):
    def __init__(self, config_file_path):
        """
        :param config_file_path: File path to the yaml file that contains all application information
        """
        if not os.path.isfile(config_file_path):
            raise FileNotFoundError("YAML configuration file not found at: " + config_file_path)

        self.yaml = yaml.load(open(config_file_path, "r"), Loader=yaml.FullLoader)

    def get_application_info(self, version_var):
        """Return the application information like Name, BuildNumber, Version and Python version in a json format"""
        app_info = ApplicationInfo()
        app_info.application_name = self.yaml["applicationName"]
        app_info.created_by = self.yaml["createdBy"]
        app_info.build_number = self.yaml["buildNumber"]
        app_info.version = version_var
        app_info.framework = "{name} {version}".format(name=self.yaml["framework"]["name"],
                                                       version=self.yaml["framework"]["version"])

        return app_info.to_json()
