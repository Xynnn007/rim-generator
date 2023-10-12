ARTIFACT_DIR := destdir

TD_SHIM_REPO_NAME := td-shim
TD_SHIM_GIT_REPO := https://github.com/confidential-containers/${TD_SHIM_REPO_NAME}.git
TD_SHIM_CODE_REV ?= 4da7dfcdd9faabd1bf9a7dc144c0206939b6d383
TD_SHIM_SAMPLE_REFERENCE_NAME := tdx.quote.body.mr_td

TD_SHIM := ${ARTIFACT_DIR}/final-boot-kernel.bin
TD_SHIM_MANIFEST := ${TD_SHIM_REPO_NAME}/td-shim-tools/src/bin/td-shim-tee-info-hash/sample_manifest.json
TD_SHIM_RAW_REFERENCE_VALUE_FILE := ${TD_SHIM_REPO_NAME}/raw_reference
TD_SHIM_SOURCE_CODE := .td-shim
TD_SHIM_SAMPLE_REFERENCE_VALUE_FILE := ${ARTIFACT_DIR}/td-shim.reference-value.sample.json

KATA_REPO_NAME := kata-containers
KATA_GIT_REPO := https://github.com/kata-containers/${KATA_REPO_NAME}.git
KATA_CODE_REV ?= 1ad87faaf

KATA_SOURCE_CODE := .${KATA_REPO_NAME}

GUEST_IMAGE := ${ARTIFACT_DIR}/kata-ubuntu-tdx.image
GUEST_IMAGE_RAW_REFERENCE_VALUE_FILE := ${KATA_REPO_NAME}/tools/osbuilder/root_hash_tdx.txt
GUEST_IMAGE_SAMPLE_REFERENCE_VALUE_FILE := ${ARTIFACT_DIR}/kata-ubuntu-tdx.image.reference-value.sample.json

KERNEL := ${ARTIFACT_DIR}/bzImage-tdx
KERNEL_SAMPLE_REFERENCE_VALUE_FILE := ${ARTIFACT_DIR}/bzImage-tdx.reference-value.sample.json

$(ARTIFACT_DIR):
	mkdir $(ARTIFACT_DIR)

$(TD_SHIM_SOURCE_CODE):
	git clone ${TD_SHIM_GIT_REPO} && cd ${TD_SHIM_REPO_NAME} && \
	git reset --hard ${TD_SHIM_CODE_REV} && \
    git submodule update --init --recursive
	touch .td-shim

$(TD_SHIM): $(TD_SHIM_SOURCE_CODE) $(ARTIFACT_DIR)
	cd ${TD_SHIM_REPO_NAME} && \
    make preparation && \
    bash sh_script/build_final.sh boot_kernel
	mv ${TD_SHIM_REPO_NAME}/target/release/final-boot-kernel.bin $(TD_SHIM)

$(TD_SHIM_RAW_REFERENCE_VALUE_FILE): $(TD_SHIM_SOURCE_CODE) $(TD_SHIM)
	cd ${TD_SHIM_REPO_NAME} && \
    cargo run -p td-shim-tools \
      --bin td-shim-tee-info-hash \
      --features tee \
      -- --manifest ../${TD_SHIM_MANIFEST} \
      --image ../${TD_SHIM} \
      --out_bin tee_info.bin 2>../tmp && \
	    cd ..
	cat tmp | grep -A 1 "MR TD:" | tail -1 > ${TD_SHIM_RAW_REFERENCE_VALUE_FILE}

$(TD_SHIM_SAMPLE_REFERENCE_VALUE_FILE): $(TD_SHIM_RAW_REFERENCE_VALUE_FILE) $(ARTIFACT_DIR)
	python $(TD_SHIM_REPO_NAME).py $(TD_SHIM_RAW_REFERENCE_VALUE_FILE) $(TD_SHIM_SAMPLE_REFERENCE_NAME) $(TD_SHIM_SAMPLE_REFERENCE_VALUE_FILE)

td-shim: $(TD_SHIM_SAMPLE_REFERENCE_VALUE_FILE) $(TD_SHIM)

$(KATA_SOURCE_CODE):
	git clone ${KATA_GIT_REPO} && \
		cd ${KATA_REPO_NAME} && \
		git reset --hard ${KATA_CODE_REV}
	touch ${KATA_SOURCE_CODE}

$(GUEST_IMAGE) $(GUEST_IMAGE_RAW_REFERENCE_VALUE_FILE) $(KERNEL): $(KATA_SOURCE_CODE) $(ARTIFACT_DIR)
	cd ${KATA_REPO_NAME} && \
    USE_CACHE=no MEASURED_ROOTFS=yes $(MAKE) rootfs-image-tdx-tarball
	mv ${KATA_REPO_NAME}/tools/packaging/kata-deploy/local-build/build/rootfs-image-tdx/destdir/opt/kata/share/kata-containers/kata-ubuntu-latest-tdx.image $(GUEST_IMAGE)
	kernel_config_version=$(shell cat $(KATA_REPO_NAME)/tools/packaging/kernel/kata_config_version); \
	kernel_version=$(shell INSTALL_IN_GOPATH=false $(KATA_REPO_NAME)/ci/install_yq.sh && yq r $(KATA_REPO_NAME)/versions.yaml assets.kernel-tdx-experimental.version); \
	cp ${KATA_REPO_NAME}/tools/packaging/kata-deploy/local-build/build/kernel-tdx-experimental/destdir/opt/kata/share/kata-containers/vmlinuz-$$kernel_version-$$kernel_config_version-tdx $(KERNEL)

$(GUEST_IMAGE_SAMPLE_REFERENCE_VALUE_FILE): $(GUEST_IMAGE_RAW_REFERENCE_VALUE_FILE) $(ARTIFACT_DIR)
	$(eval REF=$(shell sh -c "cat ${GUEST_IMAGE_RAW_REFERENCE_VALUE_FILE} | grep Root" | awk '{print $$3}'))
	python guest-image.py ${REF} $(GUEST_IMAGE_SAMPLE_REFERENCE_VALUE_FILE)

$(KERNEL_SAMPLE_REFERENCE_VALUE_FILE): $(KERNEL) $(TD_SHIM_SOURCE_CODE) $(ARTIFACT_DIR)
	$(eval SIZE=$(shell sh -c "cat $(TD_SHIM_REPO_NAME)/devtools/td-layout-config/config_memory_linux.json | jq '.memory_regions[4].size'"))
	python kernel.py $(KERNEL) ${SIZE} $(KERNEL_SAMPLE_REFERENCE_VALUE_FILE)

guest-image: $(GUEST_IMAGE) $(GUEST_IMAGE_SAMPLE_REFERENCE_VALUE_FILE)

kernel: $(KERNEL) $(KERNEL_SAMPLE_REFERENCE_VALUE_FILE)

release: td-shim guest-image kernel
	@echo "Build done!"

clean:
	rm -rf $(TD_SHIM_SOURCE_CODE) $(TD_SHIM_SAMPLE_REFERENCE_VALUE_FILE) \
		$(TD_SHIM_REPO_NAME) $(KATA_SOURCE_CODE) $(GUEST_IMAGE_SAMPLE_REFERENCE_VALUE_FILE) \
		$(KATA_REPO_NAME) $(GUEST_IMAGE) \
		$(KERNEL) $(KERNEL_SAMPLE_REFERENCE_VALUE_FILE) \
		$(ARTIFACT_DIR)
