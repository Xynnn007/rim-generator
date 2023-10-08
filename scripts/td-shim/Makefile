REPO_NAME := td-shim
GIT_REPO := https://github.com/confidential-containers/${REPO_NAME}.git
TD_SHIM_CODE_REV ?=
SAMPLE_REFERENCE_NAME := tdx.quote.body.mr_td

ARTIFACT := ${REPO_NAME}/target/release/final-boot-kernel.bin
MANIFEST := ${REPO_NAME}/
RAW_REFERENCE_VALUE_FILE := ${REPO_NAME}/raw_reference
SAMPLE_REFERENCE_VALUE_FILE := ${REPO_NAME}/td-shim-tools/src/bin/td-shim-tee-info-hash/sample_manifest.json
SOURCE_CODE := .td-shim
SAMPLE_REFERENCE_FILE := td-shim.reference-value.sample.json

$(SOURCE_CODE):
	git clone ${GIT_REPO} && cd ${REPO_NAME} && \
    git submodule update --init --recursive
	touch .td-shim

$(ARTIFACT): $(SOURCE_CODE)
	cd ${REPO_NAME} && \
    make preparation && \
    bash sh_script/build_final.sh boot_kernel

$(RAW_REFERENCE_VALUE_FILE): $(SOURCE_CODE) $(ARTIFACT)
	cd ${REPO_NAME} && \
    cargo run -p td-shim-tools \
      --bin td-shim-tee-info-hash \
      --features tee \
      -- --manifest ../${SAMPLE_REFERENCE_VALUE_FILE} \
      --image ../${ARTIFACT} \
      --out_bin tee_info.bin 2>../tmp && \
	    cd ..
	cat tmp | grep -A 1 "MR TD:" | tail -1 > ${RAW_REFERENCE_VALUE_FILE}

$(SAMPLE_REFERENCE_VALUE_FILE): $(RAW_REFERENCE_VALUE_FILE)
	python sample_ref.py $(RAW_REFERENCE_VALUE_FILE) $(SAMPLE_REFERENCE_NAME) $(SAMPLE_REFERENCE_FILE)

release: $(ARTIFACT) $(SAMPLE_REFERENCE_VALUE_FILE)
	echo "Build done!"

clean:
	rm -rf $(SOURCE_CODE) $(SAMPLE_REFERENCE_VALUE_FILE) $(REPO_NAME)
