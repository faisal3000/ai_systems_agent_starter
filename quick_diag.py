"""Run me from the project root (venv active)."""

import pathlib, sqlite3, sys
from passlib.context import CryptContext

DB   = pathlib.Path("users.db").resolve()
MAIL = "f.khann@gmail.com"
RAW  = "Passw0rd!"
CTX  = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

with sqlite3.connect(DB) as con:
    row = con.execute(
        "SELECT id, email, password, is_active, is_admin FROM users WHERE email=?",
        (MAIL,),
    ).fetchone()

print("\nusers.db ➜", DB)
print("row ➜", row)

if not row:
    sys.exit("\n❌  No row – run  fix_users.py  then restart Uvicorn\n")

if not CTX.verify(RAW, row[2]):
    sys.exit("\n❌  Hash mismatch – stored password isn’t 'Passw0rd!'\n")

if not row[3]:
    sys.exit("\n❌  is_active = 0 – account disabled\n")

print("\n✅  Row is fine – any 401 now comes from the request payload.\n")
