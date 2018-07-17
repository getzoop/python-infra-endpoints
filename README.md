# Zoop Python Infrastructure Endpoints (zpi)

This library deliveries a simple way to give your python app all formatted data to create two restful endpoints for obtain data about application's info and health routes.



## Application Info

### Response Example
```json
{
  "applicationName": "Zoop Subscription",
  "createdBy": "Build Tool",
  "version": "1.7.2-626-3d9eb36",
  "buildNumber": "20180713-001",
  "framework": "Falcon 1.1.0",
  "pythonVersion": "3.5.5 (default, Feb  6 2018, 10:57:32) [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)]"
}
```

#### Status
Application info always return 200 Ok.

#### Objective
When called, this route should return information about the application's package construction.

#### Response body explained
The response object have this following fields:

- _applicationName_: your application name (replacing blank spaces for dashes, accented characters for unaccented characters and omitting special characters).
- _createdBy_: name and version of your build tool. If no one are used, you can specify the CI server name and version.
- _version_: your application version, may be `{major}.{minor}.{release}` pattern or a git hash from repository.
- _buildNumber_: the date and the CI build number where it's possible to find the artifacts of this deployment. Preferable that it be in the following pattern: `yyyyMMdd-{CI-BUILD_NUMBER}`.
- _framework_: name and version of the framework used in the project. 

### How to configure 

#### Configuration file
First you must create a YAML file containing the following structure: 
```yaml
applicationName: Zoop Subscription
createdBy: Build Tool
buildNumber: 20180713-001
version: 1.7.2-626-3d9eb36
framework:
  name: Falcon
  version: 1.1.0
```

#### Build Number
You can configure a target in your Makefile to generate a build number, just add the following line to the Makefile and configure the path to the yaml config file and he will update the build number every build you make.

```makefile
generateBuildNumber:
	$(eval BUILD_SUFFIX := $(shell python -c "import datetime; print(f\"\{datetime.datetime.now():%Y%m%d\}\")"))
	-sed -i "/buildNumber:/c buildNumber: $(BUILD_SUFFIX)-$(CI_BUILD_NUMBER)" $(YAML_CONFIG_FILE_PATH)
```

#### Version Number
For version number, you should create a tag in the project's git repository and run the make target below, he will update the yaml file with the lastest tag version.

```makefile
generateVersion:
	$(eval VERSION := $(shell echo "1.7.2-626-3d9eb36"))
	-sed -i "/version:/c version: $(VERSION)" $(YAML_CONFIG_FILE_PATH)
```

#### Adding route
Add a `/info` route to you web framework and use the class `InfoInfrastructure` to load all information and return as json in the desired format, like the exemple using `Falcon 1.1.0` below:

```python 
from zpi.info import InfoInfrastructure

class InfoResource(object):

    def on_get(self, req, resp):
        info = InfoInfrastructure(os.path.abspath("app/config/settings/info.yml"))
        resp.body = info.info()
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

        def check_payments_api_health():
            service = PaymentsService()
            return service.healthcheck(ApiEnum.PAYMENTS)

        def check_zoop_api_health():
            service = PaymentsService()
            return service.healthcheck(ApiEnum.ZOOP_API)

        def check_database_connectivity():
            repository = HealthcheckRepository()
            return repository.check_connectivity()

        health.add_dependency("MySQL Database", True, check_database_connectivity)
        health.add_dependency("Payments API", True, check_payments_api_health)
        health.add_dependency("Zoop API", True, check_zoop_api_health)

        health.validate_dependencies()

        resp.body = health.health.to_json()
        resp.status = falcon.HTTP_200
```
##### Step By Step

- The method `register_dependency` receives 3 arguments:
	- _name_: Dependency's name.
	- _is_critical_: Boolean indicating if this dependency is critical to application.
	- _validation_method_: Function without arguments who will perform a validation and return a Boolean indicating if the dependency is UP or DOWN.

- The method `validate_dependencies` execute all validation method from registered dependencies and assess, based on which dependencies is UP or DOWN, the application health.

- The method `health.health.to_json()` get all information gathered and transform in a [JSON](#health-response-example).