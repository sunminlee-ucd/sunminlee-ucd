"""Measure this local SQLite example; never a production service benchmark."""
import argparse
import json
import math
import platform
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path

from refresh_sessions import SessionStore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=200)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.iterations < 1:
        parser.error('--iterations must be positive')

    samples = []
    with tempfile.TemporaryDirectory() as tmp:
        store = SessionStore(str(Path(tmp)/'benchmark.sqlite'))
        settings = {
            'journal_mode': store.db.execute('PRAGMA journal_mode').fetchone()[0],
            'synchronous': store.db.execute('PRAGMA synchronous').fetchone()[0],
        }
        try:
            for index in range(args.iterations):
                original = store.issue(user_id=1, now=index*10)
                start = time.perf_counter_ns()
                replacement = store.rotate(original, now=index*10+1)
                samples.append((time.perf_counter_ns()-start)/1_000_000)
                store.logout(replacement, now=index*10+2)
        finally:
            store.close()
    ordered = sorted(samples)
    report = {
        'scope': 'Standalone adaptation: serial file-backed SQLite refresh rotation and commit',
        'not_measured': ['production PostgreSQL', 'HTTP latency', 'JWT signing', 'load capacity'],
        'environment': {'python': platform.python_version(), 'platform': platform.platform(),
                        'sqlite': sqlite3.sqlite_version, **settings},
        'iterations': len(samples),
        'units': 'milliseconds',
        'p50': statistics.median(samples),
        'p95_nearest_rank': ordered[math.ceil(len(ordered)*0.95)-1],
        'mean': statistics.mean(samples),
        'samples': samples,
    }
    rendered = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'samples'}, indent=2))


if __name__ == '__main__':
    main()
