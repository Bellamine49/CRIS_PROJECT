import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "cle-secrete-temporaire-a-changer"

def email_valide(email):
    return re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", email) is not None

def db():
    conn = sqlite3.connect("cris.db")
    conn.row_factory = sqlite3.Row
    return conn

def trouver_utilisateur(email):
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def admin_requis():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        abort(403)
    return None

@app.route("/", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        if not email_valide(email):
            message = "Email invalide."
        else:
            user = trouver_utilisateur(email)
            if user is None or not check_password_hash(user["password_hash"], password):
                message = "Email ou mot de passe incorrect."
            else:
                session["user_id"] = user["id"]
                session["email"] = user["email"]
                session["role"] = user["role"]
                return redirect(url_for("espace"))
    return render_template("login.html", message=message)

@app.route("/espace")
def espace():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("espace.html", email=session["email"], role=session["role"])

@app.route("/admin")
def admin():
    refus = admin_requis()
    if refus:
        return refus
    conn = db()
    users = conn.execute("SELECT id, email, role FROM users ORDER BY id").fetchall()
    conn.close()
    return render_template("admin.html", email=session["email"], users=users,
                           message=request.args.get("message"))

@app.route("/admin/creer", methods=["POST"])
def admin_creer():
    refus = admin_requis()
    if refus:
        return refus
    email = request.form["email"].strip()
    password = request.form["password"]
    role = request.form["role"]
    if role not in ("user", "admin"):
        role = "user"
    if not email_valide(email) or len(password) < 6:
        return redirect(url_for("admin", message="Email invalide ou mot de passe trop court (6 minimum)."))
    conn = db()
    try:
        conn.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                     (email, generate_password_hash(password), role))
        conn.commit()
        msg = "Utilisateur créé."
    except sqlite3.IntegrityError:
        msg = "Cet email existe déjà."
    conn.close()
    return redirect(url_for("admin", message=msg))

@app.route("/admin/modifier/<int:user_id>", methods=["POST"])
def admin_modifier(user_id):
    refus = admin_requis()
    if refus:
        return refus
    if user_id == session["user_id"]:
        return redirect(url_for("admin", message="Tu ne peux pas changer ton propre rôle."))
    role = request.form["role"]
    if role not in ("user", "admin"):
        role = "user"
    conn = db()
    conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin", message="Rôle modifié."))

@app.route("/admin/supprimer/<int:user_id>", methods=["POST"])
def admin_supprimer(user_id):
    refus = admin_requis()
    if refus:
        return refus
    if user_id == session["user_id"]:
        return redirect(url_for("admin", message="Tu ne peux pas te supprimer toi-même."))
    conn = db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin", message="Utilisateur supprimé."))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
