"""
fix_hash.py – writes a pbkdf2_sha256 hash for Passw0rd!
Run once inside backend/.venv, from the backend folder.
"""

from passlib.context import CryptContext
import sqlite3, pathlib

pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
hashed = pwd.hash("Passw0rd!")

db = pathlib.Path("..", "systems_engineering.db")   # project-root DB
con = sqlite3.connect(db)

con.execute("""
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE,
  hashed_password TEXT,
  is_confirmed INTEGER DEFAULT 0,
  is_approved  INTEGER DEFAULT 0,
  is_admin     INTEGER DEFAULT 0,
  name TEXT,
  company_name TEXT
);
""")

con.execute("""
INSERT INTO users (email, hashed_password, is_admin, is_confirmed, is_approved)
VALUES (?, ?, 1, 1, 1)
ON CONFLICT(email) DO UPDATE
  SET hashed_password = excluded.hashed_password,
      is_admin=1, is_confirmed=1, is_approved=1;
""", ("f.khann@gmail.com", hashed))

con.commit(); con.close()
print("✅  Hash written – you can now log in with Passw0rd!")
