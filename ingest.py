#!/usr/bin/env python3
"""Simple ingest demo: normalize sample play events and write an append-only ledger (ledger.json).
Usage: python ingest.py
"""
import os, json, hashlib, time
from pathlib import Path

sample_dir = Path(__file__).parent / "sample-data"
sample_dir.mkdir(parents=True, exist_ok=True)
plays_csv = sample_dir / "plays.csv"

# If no sample CSV exists, create a tiny sample
if not plays_csv.exists():
    plays = [
        {"isrc":"US-S1Z-99-00001","title":"Track A","artist":"Artist X","plays":120,"revenue_sats":12000},
        {"isrc":"US-S1Z-99-00002","title":"Track B","artist":"Artist Y","plays":75,"revenue_sats":7500},
    ]
    with plays_csv.open("w") as f:
        f.write("isrc,title,artist,plays,revenue_sats\n")
        for p in plays:
            f.write(f"{p['isrc']},{p['title']},{p['artist']},{p['plays']},{p['revenue_sats']}\n")

# Read CSV and create ledger entries
ledger_path = Path(__file__).parent / "ledger.json"
entries = []
with plays_csv.open() as f:
    header = f.readline().strip().split(",")
    for line in f:
        cols = line.strip().split(",")
        row = dict(zip(header, cols))
        # normalize types
        row["plays"] = int(row["plays"]) 
        row["revenue_sats"] = int(row["revenue_sats"]) 
        row["timestamp"] = int(time.time())
        # compute tamper-evident hash for the entry
        h = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
        row["entry_hash"] = h
        entries.append(row)

# Append to ledger (create if missing)
if ledger_path.exists():
    with ledger_path.open() as f:
        existing = json.load(f)
else:
    existing = []

existing.extend(entries)
with ledger_path.open("w") as f:
    json.dump(existing, f, indent=2)

print(f"Wrote {len(entries)} entries to {ledger_path}")
