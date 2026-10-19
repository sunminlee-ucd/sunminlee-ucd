import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from refresh_sessions import SessionRejected, SessionStore, token_hash


class RefreshSessionTests(unittest.TestCase):
    def setUp(self):
        self.store = SessionStore()
        self.addCleanup(self.store.close)

    def test_storage_keeps_a_hash_instead_of_the_returned_token(self):
        raw = self.store.issue(1, now=100)
        row = self.store.snapshot()[0]
        self.assertEqual(row['token_hash'], token_hash(raw))
        self.assertNotIn(raw, str(row))

    def test_rotation_preserves_absolute_expiry_and_links_replacement(self):
        first = self.store.issue(1, now=100)
        second = self.store.rotate(first, now=1000)
        rows = self.store.snapshot()
        self.assertNotEqual(first, second)
        self.assertEqual(rows[0]['revoked_at'], 1000)
        self.assertEqual(rows[0]['replaced_by_token_hash'], token_hash(second))
        self.assertEqual(rows[0]['family_id'], rows[1]['family_id'])
        self.assertEqual(rows[0]['expires_at'], rows[1]['expires_at'])

    def test_replay_revocation_survives_the_rejected_request(self):
        first = self.store.issue(1, now=100)
        second = self.store.rotate(first, now=200)
        third = self.store.rotate(second, now=300)
        with self.assertRaisesRegex(SessionRejected, 'reuse_detected'):
            self.store.rotate(first, now=400)
        self.assertTrue(all(r['revoked_at'] is not None for r in self.store.snapshot()))
        with self.assertRaises(SessionRejected):
            self.store.rotate(third, now=401)

    def test_replay_does_not_revoke_an_independent_login_family(self):
        first = self.store.issue(1, now=100)
        independent = self.store.issue(1, now=101)
        self.store.rotate(first, now=200)
        with self.assertRaises(SessionRejected):
            self.store.rotate(first, now=300)
        self.store.rotate(independent, now=301)

    def test_expiry_boundary_rejects_and_persists_revocation(self):
        raw = self.store.issue(1, now=100)
        expiry = self.store.snapshot()[0]['expires_at']
        with self.assertRaisesRegex(SessionRejected, 'expired'):
            self.store.rotate(raw, now=expiry)
        self.assertEqual(self.store.snapshot()[0]['revoked_at'], expiry)

    def test_remember_me_selects_thirty_days_instead_of_seven(self):
        self.store.issue(1, now=100)
        self.store.issue(1, now=100, remember_me=True)
        self.assertEqual([r['expires_at']-100 for r in self.store.snapshot()],
                         [7*86400, 30*86400])

    def test_logout_with_an_old_token_revokes_its_current_descendant(self):
        first = self.store.issue(1, now=100)
        replacement = self.store.rotate(first, now=200)
        self.store.logout(first, now=300)
        with self.assertRaises(SessionRejected):
            self.store.rotate(replacement, now=301)

    def test_unknown_token_changes_no_existing_sessions(self):
        self.store.issue(1, now=100)
        before = self.store.snapshot()
        with self.assertRaisesRegex(SessionRejected, 'unknown_token'):
            self.store.rotate('synthetic-unknown', now=200)
        self.store.logout('synthetic-unknown', now=201)
        self.assertEqual(before, self.store.snapshot())

    def test_failed_replacement_insert_rolls_back_without_consuming_original(self):
        store = SessionStore(token_factory=lambda: 'synthetic-fixed-token')
        self.addCleanup(store.close)
        original = store.issue(1, now=100)
        with self.assertRaises(sqlite3.IntegrityError):
            store.rotate(original, now=200)
        self.assertEqual(len(store.snapshot()), 1)
        self.assertIsNone(store.snapshot()[0]['revoked_at'])
        store.token_factory = lambda: 'synthetic-new-token'
        self.assertEqual(store.rotate(original, now=201), 'synthetic-new-token')

    def test_rotation_and_revocation_persist_across_reopening_the_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp)/'sessions.sqlite')
            first = SessionStore(path)
            raw = first.issue(1, now=100)
            replacement = first.rotate(raw, now=200)
            first.close()
            second = SessionStore(path)
            try:
                with self.assertRaises(SessionRejected):
                    second.rotate(raw, now=300)
                with self.assertRaises(SessionRejected):
                    second.rotate(replacement, now=301)
            finally:
                second.close()

    def test_two_connections_cannot_both_accept_the_same_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp)/'sessions.sqlite')
            seed = SessionStore(path)
            raw = seed.issue(1, now=100)
            seed.close()
            barrier = threading.Barrier(2)
            outcomes = []

            def refresh():
                store = SessionStore(path)
                try:
                    barrier.wait(timeout=5)
                    store.rotate(raw, now=200)
                    outcomes.append('accepted')
                except SessionRejected as error:
                    outcomes.append(str(error))
                except Exception as error:
                    outcomes.append(type(error).__name__)
                finally:
                    store.close()

            threads = [threading.Thread(target=refresh) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=10)
                self.assertFalse(thread.is_alive())
            self.assertCountEqual(outcomes, ['accepted', 'reuse_detected'])
            final = SessionStore(path)
            try:
                self.assertTrue(all(r['revoked_at'] is not None for r in final.snapshot()))
            finally:
                final.close()


if __name__ == '__main__':
    unittest.main()
