#!/usr/bin/env python3
"""Simple cross-domain indexer: builds an inverted index from two sample datasets and links by ISRC.
Usage: python index_crossdomain.py
"""
import json
from pathlib import Path

out = Path(__file__).parent
# sample datasets
meta = [
    {"id":"m1","isrc":"US-S1Z-99-00001","title":"Track A","artist":"Artist X"},
    {"id":"m2","isrc":"US-S1Z-99-00002","title":"Track B","artist":"Artist Y"},
]
other = [
    {"id":"d1","isrc":"US-S1Z-99-00001","external_source":"label-db","royalty_pct":70},
    {"id":"d2","isrc":"US-S1Z-99-00003","external_source":"aggregator","royalty_pct":65},
]

# build inverted index for titles and artists
index = {}
for m in meta:
    for term in (m['title']+" "+m['artist']).lower().split():
        index.setdefault(term, []).append(m['id'])

# cross-domain linking by ISRC
links = {}
for m in meta:
    isrc = m['isrc']
    linked = [d for d in other if d.get('isrc') == isrc]
    if linked:
        links[m['id']] = linked

with (out / 'cross_index.json').open('w') as f:
    json.dump({'inverted_index': index, 'links': links}, f, indent=2)

print(f"Wrote cross-domain index to {out / 'cross_index.json'}")
