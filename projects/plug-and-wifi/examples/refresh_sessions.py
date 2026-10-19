"""Standalone adaptation of Plug & Wifi's refresh-token lifecycle.

Uses a SQLite transaction instead of the application's SQLAlchemy row lock.
This example does not issue JWTs or implement a complete login service.
"""
import hashlib
import secrets
import sqlite3
import uuid


class SessionRejected(Exception):
    pass


def token_hash(raw_token):
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


class SessionStore:
    def __init__(self, path=":memory:", token_factory=None):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.token_factory = token_factory or (lambda: secrets.token_urlsafe(48))
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                family_id TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                revoked_at INTEGER,
                replaced_by_token_hash TEXT
            );
            CREATE INDEX IF NOT EXISTS family_index ON sessions(family_id);
        """)

    def close(self):
        self.db.close()

    def _insert(self, user_id, family_id, now, expires_at):
        raw = self.token_factory()
        self.db.execute(
            "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, NULL, NULL)",
            (token_hash(raw), user_id, family_id, now, expires_at),
        )
        return raw

    def issue(self, user_id, now, remember_me=False):
        lifetime = (30 if remember_me else 7) * 24 * 60 * 60
        return self._insert(user_id, str(uuid.uuid4()), now, now + lifetime)

    def _revoke_family(self, family_id, now):
        self.db.execute(
            "UPDATE sessions SET revoked_at = ? "
            "WHERE family_id = ? AND revoked_at IS NULL",
            (now, family_id),
        )

    def rotate(self, raw_token, now):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute(
                "SELECT * FROM sessions WHERE token_hash = ?",
                (token_hash(raw_token),),
            ).fetchone()
            if row is None:
                raise SessionRejected("unknown_token")
            if row["revoked_at"] is not None:
                self._revoke_family(row["family_id"], now)
                # Revocation must survive the rejected request.
                self.db.commit()
                raise SessionRejected("reuse_detected")
            if row["expires_at"] <= now:
                self.db.execute(
                    "UPDATE sessions SET revoked_at = ? WHERE token_hash = ?",
                    (now, row["token_hash"]),
                )
                self.db.commit()
                raise SessionRejected("expired")

            replacement = self._insert(
                row["user_id"], row["family_id"], now, row["expires_at"]
            )
            self.db.execute(
                "UPDATE sessions SET revoked_at = ?, replaced_by_token_hash = ? "
                "WHERE token_hash = ?",
                (now, token_hash(replacement), row["token_hash"]),
            )
            self.db.commit()
            return replacement
        except Exception:
            if self.db.in_transaction:
                self.db.rollback()
            raise

    def logout(self, raw_token, now):
        row = self.db.execute(
            "SELECT family_id FROM sessions WHERE token_hash = ?",
            (token_hash(raw_token),),
        ).fetchone()
        if row is not None:
            self._revoke_family(row["family_id"], now)

    def snapshot(self):
        """Return storage rows for synthetic tests and demonstrations only."""
        return [dict(row) for row in self.db.execute(
            "SELECT * FROM sessions ORDER BY created_at, rowid"
        )]
