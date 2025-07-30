import sqlite3, pathlib, bcrypt, textwrap

db = pathlib.Path("systems_engineering.db")
con = sqlite3.connect(db)

con.executescript(textwrap.dedent("""
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
"""))

pw_hash = bcrypt.hashpw(b"Passw0rd!", bcrypt.gensalt(12)).decode()

con.execute("""
INSERT INTO users (email, hashed_password, is_admin, is_confirmed, is_approved)
VALUES (?, ?, 1, 1, 1)
ON CONFLICT(email) DO UPDATE
  SET hashed_password = excluded.hashed_password,
      is_admin        = 1,
      is_confirmed    = 1,
      is_approved     = 1;
""", ("f.khann@gmail.com", pw_hash))

con.commit()
print("✅  DB & user ready (rows changed:", con.total_changes, ")")
con.close()
