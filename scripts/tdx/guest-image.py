#!/usr/bin/env python
# coding=utf-8
# Copyright (c) 2023, Alibaba Inc.

# Usage: python simple_ref.py <path-to-raw-mrtd-file> <name-of-reference-value> <output-file>

import json
import sys

sys.path.append('../')

import lib

SAMPLE_REFERENCE_HASH = "tdx.ccel.kernel_parameters.cc_rootfs_verity.hash"
SAMPLE_REFERENCE_SCHEME = "tdx.ccel.kernel_parameters.cc_rootfs_verity.scheme"
SAMPLE_REFERENCE_SCHEME_VALUE = "dm-verity"

def main():
    if len(sys.argv) != 3:
        print("illegal input args")
        exit(-1)

    root_hash = sys.argv[1]
    output = sys.argv[2]

    struct = {
        SAMPLE_REFERENCE_HASH: [root_hash],
        SAMPLE_REFERENCE_SCHEME: [SAMPLE_REFERENCE_SCHEME_VALUE]
    }
    provenance = lib.generate_sample_provenance(struct)
    with open(output, 'w+') as outfile:
        outfile.write(provenance)

main()
