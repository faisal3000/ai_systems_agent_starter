"""
backend/scripts/create_super_user.py
------------------------------------
Creates / updates a super-user account (f.khann@gmail.com) in the local
SQLite DB.  Safe to run many times – it just keeps the row up-to-date.
"""

import sqlite3
from pathlib import Path
import textwrap
import sys

# ── locate the DB ──────────────────────────────────────────────────────
DB_FILE = Path(__file__).resolve().parent.parent / "systems_engineering.db"
if not DB_FILE.exists():
    sys.exit(f"❌  {DB_FILE} not found – start the backend at least once so the DB is created.")

# bcrypt-hash for the password  "Passw0rd!"
HASH = "$2b$12$qsnXgAbcz2e3YOXx.oZA1O4l7AFihb8X6V4H1LppYHSW7yVk5NZuW"

SQL = textwrap.dedent(f"""
    CREATE TABLE IF NOT EXISTS users(
      id             INTEGER PRIMARY KEY AUTOINCREMENT,
      email          TEXT UNIQUE,
      hashed_password TEXT,
      is_confirmed   INTEGER DEFAULT 0,
      is_approved    INTEGER DEFAULT 0,
      is_admin       INTEGER DEFAULT 0,
      name           TEXT,
      company_name   TEXT
    );

    INSERT INTO users (email, hashed_password, is_admin, is_confirmed, is_approved)
    VALUES ('f.khann@gmail.com', '{HASH}', 1, 1, 1)
    ON CONFLICT(email) DO UPDATE
      SET is_admin=1,
          is_confirmed=1,
          is_approved=1;
""")

# ── run the script ─────────────────────────────────────────────────────
with sqlite3.connect(DB_FILE) as con:
    con.executescript(SQL)
    con.commit()

print("✅  super-user ready – you can now log in as f.khann@gmail.com / Passw0rd!")
