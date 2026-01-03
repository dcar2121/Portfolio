#!/usr/bin/env python3
"""Simple reconciliation demo: compare expected payouts to ledger totals.
Usage: python reconcile.py
"""
import json
from pathlib import Path

ledger_path = Path(__file__).parent / "ledger.json"
if not ledger_path.exists():
    print("Ledger not found. Run ingest.py first.")
    raise SystemExit(1)

with ledger_path.open() as f:
    ledger = json.load(f)

# Sum revenue per ISRC
totals = {}
for e in ledger:
    isrc = e.get("isrc")
    totals.setdefault(isrc, 0)
    totals[isrc] += int(e.get("revenue_sats", 0))

# For demo, expected payouts are derived from totals with multiplier (simulate fees/deductions)
report = []
for isrc, sats in totals.items():
    expected = sats
    paid = int(sats * 0.98)  # simulate 2% withheld/fees
    report.append({"isrc": isrc, "expected_sats": expected, "paid_sats": paid, "delta": expected - paid})

out = Path(__file__).parent / "reconciliation_report.json"
with out.open("w") as f:
    json.dump(report, f, indent=2)

print(f"Wrote reconciliation report to {out}")
