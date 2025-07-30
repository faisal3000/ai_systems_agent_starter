# inspect_db.py  – quick peek at the users table
import sqlite3, pathlib, pprint

db = pathlib.Path("users.db")          # project-root file
con = sqlite3.connect(db)

rows = con.execute(
    "SELECT id, email, password, is_active, is_admin FROM users"
).fetchall()
pprint.pprint(rows)

con.close()
