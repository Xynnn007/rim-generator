#!/usr/bin/env python
# coding=utf-8
# Copyright (c) 2023, Alibaba Inc.

# Usage: python kernel.py <path-to-kernel> <length-of-payload-defined-intd-shim> <output-file>

import sys
import hashlib

sys.path.append('../')

import lib

SAMPLE_REFERENCE_HASH = "tdx.ccel.kernel"
PAYLOAD_LENGTH = eval(sys.argv[2])

def kernel_hash(kernel_file):
    hashbuf = hashlib.sha384()
    with open(kernel_file, 'rb') as kernel:
        content = kernel.read()
        padding_length = PAYLOAD_LENGTH - len(content)
        if padding_length < 0:
            exit(-1)
        hashbuf.update(content)
        hashbuf.update(b'\0' * padding_length)
    return hashbuf.hexdigest()

def main():
    if len(sys.argv) != 4:
        print("illegal input args")
        exit(-1)

    kernel_file = sys.argv[1]
    output = sys.argv[3]

    struct = {
        SAMPLE_REFERENCE_HASH: [kernel_hash(kernel_file)]
    }
    provenance = lib.generate_sample_provenance(struct)
    with open(output, 'w+') as outfile:
        outfile.write(provenance)

main()
