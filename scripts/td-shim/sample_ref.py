#!/usr/bin/env python
# coding=utf-8
# Copyright (c) 2023, Alibaba Inc.

# Usage: python simple_ref.py <path-to-raw-mrtd-file> <name-of-reference-value> <output-file>

import base64
import json
import sys

import ..lib

def main():
    if len(sys.argv) != 4:
        print("illegal input args")
        exit(-1)

    raw_path = sys.argv[1]
    name = sys.argv[2]
    output = sys.argv[3]

    with open(raw_path, 'r') as input_file:
        content_with_prefix = input_file.read()
        reference_value = get_reference_value(content_with_prefix)
        provenance = lib.generate_sample_provenance({name: [reference_value]})
        with open(output, 'w+') as outfile:
            outfile.write(provenance)

def get_reference_value(content_with_prefix):
    output_digest = ""
    content = content_with_prefix.strip()
    for byte_hex in content[1:-1].split(', '):
        if len(byte_hex) < 2:
            output_digest = output_digest + '0' + byte_hex
        else:
            output_digest = output_digest + byte_hex
    return output_digest

main()
