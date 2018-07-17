import os

from zpi.health import HealthInfrastructure
from zpi.info import InfoInfrastructure

app = HealthInfrastructure()
info = InfoInfrastructure(os.path.abspath("./infrastructure_config.yaml"))
info.get_application_info()


def checkHTTP():
    return True


def checkHTTP2():
    return False


def checkHTTP3():
    return True


app.register_dependency("Test 1", True, checkHTTP)
app.register_dependency("Test 2", False, checkHTTP2)
app.register_dependency("Test 3", True, checkHTTP3)
app.register_dependency("Test 3", False, checkHTTP3)
app.validate_dependencies()
print("-------------------- HEALTH ------------------")
print(app.__health.to_json())
print("-------------------- INFO-- ------------------")
print(info.get_application_info())
