# Local measurement: refresh-session adaptation

Recorded on 19 October 2026. [Full environment and all 200 measurements](refresh-benchmark.json).

```sh
cd projects/plug-and-wifi/examples
python benchmark.py --iterations 200 --output ../results/local-run.json
```

| Measurement | Recorded value |
| --- | ---: |
| Serial rotation operations | 200 |
| Median (p50) | 1.256378 ms |
| p95, nearest-rank method | 1.939477 ms |
| Mean | 1.325503635 ms |

Environment: Python 3.12.14, SQLite 3.53.1, Linux x86_64. A temporary file-backed database used `journal_mode=delete` and `synchronous=2` (FULL), read from SQLite pragmas. Token generation, hashing, the rotation transaction, and its commit are inside the timed interval; initial issuance and subsequent logout are outside it.

These are measurements of the standalone SQLite adaptation on one machine. They are **not HTTP latency, PostgreSQL performance, JWT-signing cost, concurrent load capacity, a customer-facing SLA, or a production improvement claim**. Different machines, storage, versions, and configurations will produce different results. There is no latency pass/fail threshold in CI.

The benchmark prints its environment and retains raw samples so its summary statistics can be independently recomputed. The executable code is in [benchmark.py](../examples/benchmark.py).
