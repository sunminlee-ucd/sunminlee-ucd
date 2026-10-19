# Refresh-session lifecycle — standalone adaptation

Adapted from my [merged refresh-token PR](https://github.com/Research-Practicum-Group-4/plugandwifi/pull/56) and the team's [reviewed API implementation](https://github.com/Research-Practicum-Group-4/plugandwifi/blob/64eacd4bf566b9e9f5c5c552b4d6f0e3ace36cdf/backend/app/main.py).

## Run

Python 3.10 or newer; standard library only. From this directory:

```sh
python -m unittest -v test_refresh_sessions
python demo.py
python benchmark.py --iterations 200 --output ../results/local-run.json
```

No application login, real account, cloud credentials, or network access is needed. Tokens are generated for the local example; the demo prints lifecycle outcomes, not token values.

## What the example proves

| Scenario | Expected behavior |
| --- | --- |
| Normal rotation | Revoke the previous token; preserve family and absolute expiry |
| Replay of a revoked token | Persist family revocation even though the request is rejected |
| Independent login | A different token family remains usable |
| Exact expiry boundary | Reject and persist expiration revocation |
| Logout using an ancestor | Revoke active descendants in that family |
| Replacement insert failure | Roll back so the original remains usable |
| Database reopened | Revocation and replacement state survive |
| Two simultaneous refresh attempts | Accept one; treat the second as replay and revoke the family |

The 11 tests also check hash-only storage, seven/thirty-day lifetimes, and unknown-token behavior.

Example console output:

```json
{"step": "rotation", "rows": 2, "expiry_preserved": true}
{"step": "replay", "result": "reuse_detected", "active_family_sessions": 0}
{"step": "replacement_after_replay", "accepted": false}
```

## Adaptation boundaries and trade-offs

- SQLite's `BEGIN IMMEDIATE` serializes writers here. The team service instead uses SQLAlchemy and a row lock on the queried session. These are different concurrency mechanisms; this test does not validate PostgreSQL behavior.
- The example uses an injected integer timestamp, local SQLite rows, and synthetic user IDs. It omits HTTP, JWT issuance, passwords, real user lookup, session cleanup, and deployment configuration.
- Family revocation is deliberately conservative: even two legitimate clients racing to refresh the same token can invalidate the replacement. Clients need to coordinate refresh attempts.
- Revocation is committed before raising the rejection. Rolling back that change together with the error would leave descendants active, which the replay test detects.
- This is an inspectable lifecycle example, not a production authentication package or a security certification.

[Recorded local measurement and raw samples](../results/README.md) · [Source-derived implementation](refresh_sessions.py)
