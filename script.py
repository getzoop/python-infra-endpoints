import os

from infrastructure.health import HealthInfrastructure
from infrastructure.info import InfoInfrastructure

app = HealthInfrastructure()
info = InfoInfrastructure(os.path.abspath("./infrastructure_config.yaml"))
info.info()


def checkHTTP():
    return True


def checkHTTP2():
    return False


def checkHTTP3():
    return True


app.add_dependency("Test 1", True, checkHTTP)
app.add_dependency("Test 2", False, checkHTTP2)
app.add_dependency("Test 3", True, checkHTTP3)
app.add_dependency("Test 3", False, checkHTTP3)
app.validate_dependencies()
print("-------------------- HEALTH ------------------")
print(app.health.to_json())
print("-------------------- INFO-- ------------------")
print(info.info())
