#!/usr/bin/env python3
"""Verify watermark sidecar HMAC.
Usage: python verify_watermark.py input_file owner_key
"""
import sys, json, hmac, hashlib
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python verify_watermark.py <input_file> <owner_key>")
    raise SystemExit(1)

infile = Path(sys.argv[1])
owner_key = sys.argv[2].encode()
watermark = infile.with_suffix(infile.suffix + ".watermark.json")
if not watermark.exists():
    print("Watermark sidecar not found.")
    raise SystemExit(1)

with watermark.open() as f:
    meta = json.load(f)

h = meta.copy()
mac = h.pop("hmac", None)
payload = json.dumps(h, sort_keys=True).encode()
calc = hmac.new(owner_key, payload, hashlib.sha256).hexdigest()
if calc == mac:
    print("Watermark valid — provenance confirmed.")
else:
    print("Watermark INVALID — provenance mismatch.")
