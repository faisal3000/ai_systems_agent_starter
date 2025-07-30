import bcrypt, sqlite3, pathlib

db   = pathlib.Path("systems_engineering.db")
con  = sqlite3.connect(db)

new_hash = bcrypt.hashpw(b"Passw0rd!", bcrypt.gensalt(12)).decode()

con.execute(
    "UPDATE users "
    "SET hashed_password = ?, is_confirmed = 1, is_approved = 1, is_admin = 1 "
    "WHERE lower(email) = lower(?)",
    (new_hash, "f.khann@gmail.com")
)
con.commit()
print("✅  rows changed:", con.total_changes)
con.close()
