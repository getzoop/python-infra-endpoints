.PHONY: all

generateBuildNumber:
	$(eval BUILD_SUFFIX := $(shell python -c "import datetime; print(f\"\{datetime.datetime.now():%Y%m%d\}\")"))
	-sed -i "/buildNumber:/c buildNumber: $(BUILD_SUFFIX)-$(CI_BUILD_NUMBER)" infrastructure_config.yaml

generateArtifactInfo: generateVersion generateBuildNumber