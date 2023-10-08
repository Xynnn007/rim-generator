#!/usr/bin/env python
# coding=utf-8
# Copyright (c) 2023, Alibaba Inc.

# Usage: python simple_ref.py <path-to-raw-mrtd-file> <name-of-reference-value> <output-file>

import base64
import json
import sys

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
        provenance = generate_sample_provenance(name, reference_value)
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

def generate_sample_message(artifact_name, reference_value):
    message = {
        artifact_name: [reference_value]
    }
    return json.dumps(message)

def generate_sample_provenance(artifact_name, reference_value):
    message = generate_sample_message(artifact_name, reference_value)
    message_bytes = message.encode("ascii")
    payload_bytes = base64.b64encode(message_bytes)
    payload_string = payload_bytes.decode("ascii")

    provenance = {
        "version" : "0.1.0",
        "type": "sample",
        "payload": payload_string
    }
    return json.dumps(provenance)
main()
