.PHONY: all
VERSION := $(shell echo "1.7.2-626-3d9eb36")
#VERSION := $(shell git describe --tags --always HEAD)

generateVersion:
	-sed -i "/version:/c version: $(VERSION)" infrastructure_config.yaml

generateBuildNumber:
	$(eval BUILD_SUFFIX := $(shell python -c "import datetime; print(f\"\{datetime.datetime.now():%Y%m%d\}\")"))
	-sed -i "/buildNumber:/c buildNumber: $(BUILD_SUFFIX)-$(CI_BUILD_NUMBER)" infrastructure_config.yaml

generateArtifactInfo: generateVersion generateBuildNumber