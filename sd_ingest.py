#!/usr/bin/env python3
"""Create a minimal sovereign data store: owner keys + entries with tamper-evidence.
Usage: python sd_ingest.py
"""
import json, secrets, hashlib, time
from pathlib import Path

out = Path(__file__).parent / "sovereign_store.json"
owners = ["publisherA@example.com", "publisherB@example.com"]
store = {"owners":{}, "entries":[]}
for o in owners:
    # generate a per-owner symmetric key (hex) — in prod use KMS
    key = secrets.token_hex(16)
    store["owners"][o] = {"key": key}

# create sample entries
for i, o in enumerate(owners, start=1):
    entry = {
        "id": f"entry-{i}",
        "owner": o,
        "payload": f"sample-data-for-{o}",
        "timestamp": int(time.time())
    }
    # tamper-evident hash
    entry_hash = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    entry["hash"] = entry_hash
    store["entries"].append(entry)

with out.open("w") as f:
    json.dump(store, f, indent=2)

print(f"Wrote sovereign store to {out}")
