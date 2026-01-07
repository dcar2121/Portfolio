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
# reconcile.py

def main():
    # Example data: replace these with your actual data sources
    expected_payouts = {
        'Artist A': 1000,
        'Artist B': 2000,
        'Artist C': 1500
    }

    ledger_totals = {
        'Artist A': 995,
        'Artist B': 2020,
        'Artist C': 1490
    }

    print("Reconciliation Report")
    print("=====================\n")
    print(f"{'Artist':<10} {'Expected':>10} {'Ledger':>10} {'Difference':>12}")

    for artist in expected_payouts:
        expected = expected_payouts.get(artist, 0)
        ledger = ledger_totals.get(artist, 0)
        diff = ledger - expected
        print(f"{artist:<10} {expected:>10} {ledger:>10} {diff:>12}")

    # Check for any discrepancies
    discrepancies = False
    for artist in expected_payouts:
        diff = ledger_totals.get(artist, 0) - expected_payouts[artist]
        if diff != 0:
            discrepancies = True

    if discrepancies:
        print("\nDiscrepancies found! Review the above differences.")
    else:
        print("\nAll payouts match ledger totals. Reconciliation complete.")

if __name__ == "__main__":
    main()
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
