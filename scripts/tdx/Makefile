REPO_NAME := kata-containers
GIT_REPO := https://github.com/kata-containers/${REPO_NAME}.git
CODE_REV ?= 1ad87faaf

ARTIFACT := ${REPO_NAME}/tools/packaging/kata-deploy/local-build/build/rootfs-image-tdx/destdir/opt/kata/share/kata-containers/kata-ubuntu-latest-tdx.image
RAW_REFERENCE_VALUE_FILE := ${REPO_NAME}/tools/osbuilder/root_hash_tdx.txt
SOURCE_CODE := .${REPO_NAME}
SAMPLE_REFERENCE_VALUE_FILE := kata-containers-tdx.img.reference-value.sample.json

$(SOURCE_CODE):
	git clone ${GIT_REPO} && \
		cd ${REPO_NAME} && \
		git reset --hard ${CODE_REV}
	touch ${SOURCE_CODE}

$(ARTIFACT) $(RAW_REFERENCE_VALUE_FILE): $(SOURCE_CODE)
	cd ${REPO_NAME} && \
    MEASURED_ROOTFS=yes $(MAKE) rootfs-image-tdx-tarball

$(SAMPLE_REFERENCE_VALUE_FILE): $(RAW_REFERENCE_VALUE_FILE)
	$(eval REF=$(shell sh -c "cat ${RAW_REFERENCE_VALUE_FILE} | grep Root" | awk '{print $$3}'))
	python image_ref.py ${REF} $(SAMPLE_REFERENCE_VALUE_FILE)

release: $(ARTIFACT) $(SAMPLE_REFERENCE_VALUE_FILE)
	@echo "Build done!"

clean:
	rm -rf $(SOURCE_CODE) $(SAMPLE_REFERENCE_VALUE_FILE) $(REPO_NAME)
