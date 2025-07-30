# ── fix_users.py  (place in project root) ───────────────────────────
"""
Creates / updates an admin user in users.db so the FastAPI login
endpoint works in local development.

Usage (from project root):
    backend\.venv\Scripts\python.exe fix_users.py
"""

from pathlib import Path
import sqlite3
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).resolve().parent          # project root
DB_PATH  = ROOT_DIR / "users.db"
CTX      = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

ADMIN_EMAIL    = "f.khann@gmail.com"
ADMIN_PASSWORD = "Passw0rd!"                        # change if desired
HASHED_PW      = CTX.hash(ADMIN_PASSWORD)

with sqlite3.connect(DB_PATH) as con:
    # ensure the table exists
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
          id         INTEGER PRIMARY KEY AUTOINCREMENT,
          email      TEXT UNIQUE,
          password   TEXT,
          is_active  INTEGER DEFAULT 0,
          is_admin   INTEGER DEFAULT 0
        );
        """
    )
    # upsert the admin row
    con.execute(
        """
        INSERT INTO users (email, password, is_active, is_admin)
        VALUES (?, ?, 1, 1)
        ON CONFLICT(email) DO UPDATE
          SET password = ?,  -- keep param order:  (email, pw, pw)
              is_active = 1,
              is_admin  = 1;
        """,
        (ADMIN_EMAIL, HASHED_PW, HASHED_PW),
    )
    con.commit()            # <-- explicit commit (best-practice)

print(f"✅  Admin '{ADMIN_EMAIL}' is ready in {DB_PATH}")
# ───────────────────────────────────────────────────────────────────
