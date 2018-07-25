import os

from zpi.health import HealthInfrastructure
from zpi.info import InfoInfrastructure

app = HealthInfrastructure()
info = InfoInfrastructure(os.path.abspath("./infrastructure_config.yaml"))
info.get_application_info()


def check_http():
    return True


def check_http2():
    return False


def check_http3():
    return True


app.register_dependency("Test 1", True, check_http)
app.register_dependency("Test 2", False, check_http2)
app.register_dependency("Test 3", True, check_http3)
app.register_dependency("Test 4", False, check_http3)

app.check_dependencies_status()
print("-------------------- HEALTH ------------------")
print(app.get_application_health_json())
print("-------------------- INFO-- ------------------")
print(info.get_application_info())
