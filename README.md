# Python Infrastructure Endpoints (zpi)

This library deliveries a simple way to give your python app all formatted data to create two restful endpoints for obtain data about application's info and health routes.

## Installation

```shell
$ pip install git+https://github.com/getzoop/python-infra-endpoints.git@releases/1.0.1#egg=zpi
```
OR add the following line to your `requirements.txt`: 
```python
git+https://github.com/getzoop/python-infra-endpoints.git@releases/1.0.1#egg=zpi
```

## Application Info

#### Response Example
```json
{
  "applicationName": "My Application Name",
  "createdBy": "Build Tool",
  "version": "1.7.2",
  "buildNumber": "20180713-001",
  "framework": "Falcon 1.1.0",
  "pythonVersion": "3.5.5 (default, Feb  6 2018, 10:57:32) [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)]"
}
```

#### Status
Application info always return 200 Ok.

#### Objective
When called, this route should return information about the application's package construction.

**Response body explained**
The response object have this following fields:

- _applicationName_: your application name (replacing blank spaces for dashes, accented characters for unaccented characters and omitting special characters).
- _createdBy_: name and version of your build tool. If no one are used, you can specify the CI server name and version.
- _version_: your application version, may be `{major}.{minor}.{release}` pattern or a git hash from repository.
- _buildNumber_: the date and the CI build number where it's possible to find the artifacts of this deployment. Preferable that it be in the following pattern: `yyyyMMdd-{CI-BUILD_NUMBER}`.
- _framework_: name and version of the framework used in the project. 

## How to configure 
 
### Configuration file
First you must create a YAML file containing the following structure: 
```yaml
applicationName: My Application Name
createdBy: Build Tool
buildNumber: 20180713-001
framework:
  name: Falcon
  version: 1.1.0
```

### Build Number
You can configure a target in your Makefile to generate a build number, just add the following line to the Makefile and configure the path to the yaml config file and he will update the build number every build you make.

```makefile
generateBuildNumber:
	$(eval BUILD_SUFFIX := $(shell python -c "import datetime; print(f\"\{datetime.datetime.now():%Y%m%d\}\")"))
	-sed -i "/buildNumber:/c buildNumber: $(BUILD_SUFFIX)-$(CI_BUILD_NUMBER)" $(YAML_CONFIG_FILE_PATH)
```

### Version Number
For version number, you should create a file named `version.py` in the root of your application main module. Inside this file you will assign a version number to a variable named `__version__` like the example below:
 ```pythonstub
 """My Application version."""
__version__ = "1.0.1"

"""Current version of My Application."""
 ```

After the version file created, you will use the console script named `zpi-increment-version` provided by this module to bump the version: 

`zpi-increment-version` help: 
```bash
$ zpi-increment-version -h
usage: zpi-increment-version [-h] [-i INCREMENTING] -f VERSION_FILE

optional arguments:
  -h, --help            show this help message and exit
  -i INCREMENTING, --increment INCREMENTING
                        Which part of application version will be incremented:
                        major, minor or release. Default: release
  -f VERSION_FILE, --version-file VERSION_FILE
                        Path to project's version.py
 
```

* To bump a release version you should execute something like: 
```bash
$ zpi-increment-version -f src/main/subscription/version.py
```
_or_
```bash
$ zpi-increment-version -i release -f src/main/subscription/version.py
```

* To bump a minor release version: 
```bash
$ zpi-increment-version -i minor -f src/main/subscription/version.py
```

* To bump a major release version: 
```bash
$ zpi-increment-version -i major -f src/main/subscription/version.py
```

The script output should be:
```
=== Incremented application version from 1.0.1 to 1.0.2 ===
=== Check version.py file to see the new __version__ value ===
```

### Adding route
Add a `/info` route to you web framework and use the class `InfoInfrastructure` to load all information and return as json in the desired format, like the exemple using `Falcon 1.1.0` below:

```python 
from zpi.info import InfoInfrastructure

class InfoResource(object):

    def on_get(self, req, resp):
        info = InfoInfrastructure(os.path.abspath("app/config/settings/info.yml"))
        resp.body = info.get_application_info()
        resp.status = falcon.HTTP_200

```

## Application Health

### Health Response Example
```json
{
  "status": "UP",
  "message": "All dependencies are up",
  "dependencies": [
    {
      "name": "My Database",
      "isCritical": true,
      "status": "UP"
    },
    {
      "name": "My 1st Http Dependency",
      "isCritical": true,
      "status": "UP"
    },
    {
      "name": "My 2nd Http Dependency",
      "isCritical": false,
      "status": "UP"
    }
  ]
}
```

### Status
Application health returns 200 for UP or PARTIAL statuses and 503 for the FAIL status.

### Objective
When called, this route should ping all the dependencies you've declared in your application: databases, filesystem directory, http dependencies, a queue, a topic, etc. Basically, these pings should garantee that application connections to dependencies are established or, at least, establishables.

### Response body explained
The response object have this following fields:

- _status_: The overall health of your application. It's an enumeration with UP, PARTIAL or FAIL as possible values
- _message_: An explanation about the status field
- _dependencies_: Dependencies declared in your application. Each dependency is a complex object that has in its structure the following fields:
name: The declared dependency name
- _isCritical_: dependency's criticity. It should be determined by its impact when out of service: if your application gets only partially impacted, it should be false, it should be true otherwise
- _status_: the health of your application connectivity with this dependency. It's an enumeration with UP or FAIL as possible values.


### Adding route
Add a `/health` route and to the follwing implementation using `HealthInfrastructure` class provided by this lib.


**Implementation Example**
```python
from zpi.health import HealthInfrastructure

class HealthResource(object):

    def on_get(self, req, resp):
        health = HealthInfrastructure()

        def check_api_health():
            service = ApiService()
            return service.healthcheck()

        def check_other_api_health():
            service = OtherApiService()
            return service.healthcheck()

        def check_database_connectivity():
            repository = HealthcheckRepository()
            return repository.check_connectivity()

        health.register_dependency("MySQL Database", True, check_database_connectivity)
        health.register_dependency("API", True, check_api_health)
        health.register_dependency("Other API", True, check_other_api_health)

        health.check_dependencies_status()

        resp.body = health.get_application_health_json()
        resp.status = falcon.HTTP_200
```
#### Step By Step

- The method `register_dependency` receives 3 arguments:
	- _name_: Dependency's name.
	- _is_critical_: Boolean indicating if this dependency is critical to application.
	- _validation_method_: Function without arguments who will perform a validation and return a Boolean indicating if the dependency is UP or DOWN.

- The method `check_dependencies_status` execute all validation method from registered dependencies and assess, based on which dependencies is UP or DOWN, the application health.

- The method `health.get_application_health_json()` get all information gathered and serialize in a [JSON](#health-response-example).


