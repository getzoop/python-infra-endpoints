import os

import zpi
from zpi.health import HealthInfrastructure
from zpi.info import InfoInfrastructure

app = HealthInfrastructure()
info = InfoInfrastructure(os.path.abspath("./infrastructure_config.yaml"))
info.get_application_info(zpi.__version__)


def checkHTTP():
    return True


def checkHTTP2():
    return False


def checkHTTP3():
    return True


app.register_dependency("Test 1", True, checkHTTP)
# app.register_dependency("Test 2", True, checkHTTP2)
app.register_dependency("Test 3", True, checkHTTP3)
# app.register_dependency("Test 3", False, checkHTTP3)
app.check_dependencies_status()
print("-------------------- HEALTH ------------------")
print(app.get_application_health_response())
print("-------------------- INFO-- ------------------")
print(info.get_application_info())
