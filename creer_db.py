import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("cris.db")
conn.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
)""")

comptes = [
    ("leyla@test.com", "Test1234", "user"),
    ("admin@test.com", "Admin1234", "admin"),
]
for email, mdp, role in comptes:
    conn.execute(
        "INSERT OR IGNORE INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        (email, generate_password_hash(mdp), role),
    )
conn.commit()

for ligne in conn.execute("SELECT id, email, role, password_hash FROM users"):
    print(ligne)
conn.close()
