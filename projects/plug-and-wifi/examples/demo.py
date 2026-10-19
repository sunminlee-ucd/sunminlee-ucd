"""Synthetic lifecycle trace; no real tokens, users, or services are printed."""
import json
from refresh_sessions import SessionRejected, SessionStore


store = SessionStore()
try:
    original = store.issue(user_id=1, now=100)
    replacement = store.rotate(original, now=200)
    before = store.snapshot()
    print(json.dumps({'step': 'rotation', 'rows': len(before),
                      'expiry_preserved': before[0]['expires_at'] == before[1]['expires_at']}))
    try:
        store.rotate(original, now=300)
    except SessionRejected as error:
        print(json.dumps({'step': 'replay', 'result': str(error),
                          'active_family_sessions': sum(r['revoked_at'] is None for r in store.snapshot())}))
    try:
        store.rotate(replacement, now=301)
    except SessionRejected:
        print(json.dumps({'step': 'replacement_after_replay', 'accepted': False}))
finally:
    store.close()
