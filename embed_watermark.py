#!/usr/bin/env python3
"""Embed a simple HMAC-based watermark as a sidecar JSON file.
Usage: python embed_watermark.py input_file owner_key
This creates input_file.watermark.json with provenance data.
"""
import sys, json, hmac, hashlib, time
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python embed_watermark.py <input_file> <owner_key>")
    raise SystemExit(1)

infile = Path(sys.argv[1])
owner_key = sys.argv[2].encode()

if not infile.exists():
    print("Input file not found; creating placeholder file.")
    infile.write_text("sample media content")

meta = {
    "filename": infile.name,
    "owner": "publisher@example.com",
    "timestamp": int(time.time()),
}
payload = json.dumps(meta, sort_keys=True).encode()
mac = hmac.new(owner_key, payload, hashlib.sha256).hexdigest()
meta["hmac"] = mac

out = infile.with_suffix(infile.suffix + ".watermark.json")
with out.open("w") as f:
    json.dump(meta, f, indent=2)

print(f"Wrote watermark sidecar: {out}")
