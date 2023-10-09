#!/usr/bin/env python
# coding=utf-8
# Copyright (c) 2023, Alibaba Inc.

# Usage: python simple_ref.py <path-to-raw-mrtd-file> <name-of-reference-value> <output-file>

import base64
import json

def generate_sample_provenance(name_value_pairs):
    message = json.dumps(name_value_pairs)
    message_bytes = message.encode("ascii")
    payload_bytes = base64.b64encode(message_bytes)
    payload_string = payload_bytes.decode("ascii")

    provenance = {
        "version" : "0.1.0",
        "type": "sample",
        "payload": payload_string
    }
    return json.dumps(provenance)
