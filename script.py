import asyncio
import os

import zpi
from zpi.health import HealthInfrastructure
from zpi.info import InfoInfrastructure

app = HealthInfrastructure()
info = InfoInfrastructure(os.path.abspath("./infrastructure_config.yaml"))


def checkHTTP():
    return True


def checkHTTP3():
    return True


async def checkHTTP2():
    return False


app.register_dependency("Sync dependency Test 1", True, checkHTTP)
app.register_dependency("Sync dependency Test 3", True, checkHTTP3)

app.check_dependencies_status()
print("-------------------- HEALTH ------------------")
print(app.get_application_health_response())
print("-------------------- INFO-- ------------------")
print(info.get_application_info(zpi.__version__))

async def test_async_dependencies():
    app.register_dependency("Sync dependency Test 1", True, checkHTTP)
    await app.register_async_dependency("Async dependency Test 2", True, checkHTTP2)
    await app.check_all_dependencies_status()
    print("-------------------- ASYNC HEALTH ------------------")
    print(app.get_application_health_response())


# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_async_dependencies())
