# backend/fix_db.py ----------------------------------------------------
# Rebuilds users.db (in project root) with one admin account
import sqlite3, pathlib, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]       # …\ai_systems_agent_starter
db   = ROOT / "users.db"                                 # <- single correct DB

sql = textwrap.dedent("""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email      TEXT UNIQUE,
      password   TEXT,
      is_active  INTEGER DEFAULT 1,
      is_admin   INTEGER DEFAULT 1
    );
    INSERT INTO users (email, password, is_active, is_admin)
    VALUES ('f.khann@gmail.com', 'Passw0rd!', 1, 1);
""")

with sqlite3.connect(db) as con:
    con.executescript(sql)

print("✅  users.db rebuilt at", db)
# ---------------------------------------------------------------------
