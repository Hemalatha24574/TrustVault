import os, sqlite3, hashlib, uuid
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "instance")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-before-deploying")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB per upload
DB_PATH = os.path.join(DATA_DIR, "trustvault.db")
ALLOWED_EXTENSIONS = {"pdf", "txt", "doc", "docx", "png", "jpg", "jpeg", "csv"}

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          password_hash TEXT NOT NULL,
          role TEXT NOT NULL DEFAULT 'user',
          company TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS documents (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          owner_id INTEGER NOT NULL REFERENCES users(id),
          company TEXT NOT NULL,
          original_name TEXT NOT NULL,
          stored_name TEXT NOT NULL,
          sha256 TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS shares (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
          user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          UNIQUE(document_id, user_id)
        );
        CREATE TABLE IF NOT EXISTS audit_logs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          actor_id INTEGER,
          actor_email TEXT NOT NULL,
          action TEXT NOT NULL,
          details TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        """)
        admin_email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
        admin_password = os.environ.get("ADMIN_PASSWORD", "")
        if admin_email and admin_password:
            found = con.execute("SELECT id FROM users WHERE email=?", (admin_email,)).fetchone()
            if not found:
                con.execute(
                    "INSERT INTO users(name,email,password_hash,role,company) VALUES(?,?,?,?,?)",
                    ("TrustVault Admin", admin_email, generate_password_hash(admin_password), "admin", "TrustVault")
                )

def audit(actor_id, actor_email, action, details):
    with db() as con:
        con.execute("INSERT INTO audit_logs(actor_id,actor_email,action,details,created_at) VALUES(?,?,?,?,?)",
                    (actor_id, actor_email, action, details[:500], datetime.now(timezone.utc).isoformat()))

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return fn(*args, **kwargs)
    return wrapped

def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def can_access(con, doc_id, user):
    doc = con.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone()
    if not doc or doc["company"].casefold() != user["company"].casefold():
        return None
    if user["role"] == "admin" or doc["owner_id"] == user["id"]:
        return doc
    share = con.execute("SELECT id FROM shares WHERE document_id=? AND user_id=?", (doc_id, user["id"])).fetchone()
    return doc if share else None

@app.context_processor
def inject_user():
    return {"current_user": session.get("name"), "current_role": session.get("role")}

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        company = request.form.get("company", "").strip()
        if not all([name, email, password, company]) or len(password) < 8:
            flash("Fill every field. Password must be at least 8 characters.")
            return render_template("register.html")
        try:
            with db() as con:
                con.execute("INSERT INTO users(name,email,password_hash,role,company) VALUES(?,?,?,?,?)",
                            (name, email, generate_password_hash(password), "user", company))
            audit(None, email, "REGISTER", f"New account registered for company {company}")
            flash("Account created. Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("That email is already registered.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with db() as con:
            user = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session.update(user_id=user["id"], name=user["name"], email=user["email"],
                           role=user["role"], company=user["company"])
            audit(user["id"], user["email"], "LOGIN", "Successful login")
            return redirect(url_for("dashboard"))
        flash("Incorrect email or password.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    audit(session["user_id"], session["email"], "LOGOUT", "User logged out")
    session.clear()
    flash("You are logged out.")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    user = dict(id=session["user_id"], role=session["role"], company=session["company"])
    with db() as con:
        if user["role"] == "admin":
            docs = con.execute("""SELECT d.*, u.name AS owner_name,
                (SELECT COUNT(*) FROM shares s WHERE s.document_id=d.id) AS share_count
                FROM documents d JOIN users u ON u.id=d.owner_id
                WHERE lower(d.company)=lower(?) ORDER BY d.id DESC""", (user["company"],)).fetchall()
            users = con.execute("SELECT id,name,email,role FROM users WHERE lower(company)=lower(?) ORDER BY id", (user["company"],)).fetchall()
        else:
            docs = con.execute("""SELECT DISTINCT d.*, u.name AS owner_name,
                (SELECT COUNT(*) FROM shares s WHERE s.document_id=d.id) AS share_count
                FROM documents d JOIN users u ON u.id=d.owner_id
                LEFT JOIN shares s ON s.document_id=d.id
                WHERE lower(d.company)=lower(?) AND (d.owner_id=? OR s.user_id=?)
                ORDER BY d.id DESC""", (user["company"], user["id"], user["id"])).fetchall()
            users = []
    return render_template("dashboard.html", docs=docs, users=users)

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    f = request.files.get("document")
    if not f or not f.filename:
        flash("Choose a file first.")
        return redirect(url_for("dashboard"))
    original = secure_filename(f.filename)
    if not original or not allowed_file(original):
        flash("File type not allowed. Use PDF, TXT, DOC/DOCX, PNG/JPG or CSV.")
        return redirect(url_for("dashboard"))
    data = f.read()
    if not data:
        flash("Empty files are not allowed.")
        return redirect(url_for("dashboard"))
    digest = hashlib.sha256(data).hexdigest()
    stored = uuid.uuid4().hex
    path = os.path.join(UPLOAD_DIR, stored)
    with open(path, "wb") as out:
        out.write(data)
    try:
        with db() as con:
            con.execute("INSERT INTO documents(owner_id,company,original_name,stored_name,sha256,created_at) VALUES(?,?,?,?,?,?)",
                        (session["user_id"], session["company"], original, stored, digest, datetime.now(timezone.utc).isoformat()))
        audit(session["user_id"], session["email"], "UPLOAD", f"Uploaded {original}; SHA-256 {digest}")
        flash("Document uploaded successfully.")
    except Exception:
        if os.path.exists(path):
            os.remove(path)
        raise
    return redirect(url_for("dashboard"))

@app.route("/share/<int:doc_id>", methods=["POST"])
@login_required
def share(doc_id):
    target_email = request.form.get("email", "").strip().lower()
    with db() as con:
        user = con.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
        doc = con.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone()
        if not doc or doc["owner_id"] != user["id"] or doc["company"].casefold() != user["company"].casefold():
            abort(403)
        target = con.execute("SELECT * FROM users WHERE email=? AND lower(company)=lower(?)",
                             (target_email, user["company"])).fetchone()
        if not target:
            flash("Recipient must have a registered account in your company.")
            return redirect(url_for("dashboard"))
        if target["id"] == user["id"]:
            flash("You already own this document.")
            return redirect(url_for("dashboard"))
        try:
            con.execute("INSERT INTO shares(document_id,user_id) VALUES(?,?)", (doc_id, target["id"]))
        except sqlite3.IntegrityError:
            pass
    audit(session["user_id"], session["email"], "SHARE", f"Shared document {doc_id} with {target_email}")
    flash("Document shared.")
    return redirect(url_for("dashboard"))

@app.route("/download/<int:doc_id>")
@login_required
def download(doc_id):
    with db() as con:
        user = con.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
        doc = can_access(con, doc_id, user)
    if not doc:
        audit(session["user_id"], session["email"], "DENIED", f"Denied access to document {doc_id}")
        abort(403)
    path = os.path.join(UPLOAD_DIR, doc["stored_name"])
    if not os.path.isfile(path):
        flash("File is missing from this deployment.")
        return redirect(url_for("dashboard"))
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    if digest != doc["sha256"]:
        audit(session["user_id"], session["email"], "INTEGRITY_FAIL", f"Hash mismatch for document {doc_id}")
        abort(409, "Document integrity check failed.")
    audit(session["user_id"], session["email"], "DOWNLOAD", f"Downloaded document {doc_id}; integrity verified")
    return send_file(path, as_attachment=True, download_name=doc["original_name"])

@app.route("/admin/audit")
@admin_required
def audit_page():
    with db() as con:
        logs = con.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 500").fetchall()
        user_count = con.execute("SELECT COUNT(*) AS n FROM users WHERE lower(company)=lower(?)", (session["company"],)).fetchone()["n"]
        doc_count = con.execute("SELECT COUNT(*) AS n FROM documents WHERE lower(company)=lower(?)", (session["company"],)).fetchone()["n"]
        share_count = con.execute("""SELECT COUNT(*) AS n FROM shares s JOIN documents d ON d.id=s.document_id
                                  WHERE lower(d.company)=lower(?)""", (session["company"],)).fetchone()["n"]
    return render_template("audit.html", logs=logs, user_count=user_count, doc_count=doc_count, share_count=share_count)

@app.errorhandler(403)
def forbidden(_):
    return render_template("error.html", code=403, message="You do not have permission to access this page or document."), 403

@app.errorhandler(409)
def conflict(err):
    return render_template("error.html", code=409, message=err.description), 409

@app.errorhandler(413)
def too_large(_):
    return render_template("error.html", code=413, message="File too large. Maximum size is 10 MB."), 413

init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
