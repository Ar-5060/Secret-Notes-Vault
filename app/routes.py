from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import create_user, get_user, add_note, get_notes
from .utils import caesar_cipher

main = Blueprint('main', __name__)

# -------- LOGIN REQUIRED ----------
def require_login():
    return 'username' in session


# -------- HOME / DASHBOARD --------
@main.route('/')
def dashboard():
    if not require_login():
        return redirect(url_for('main.login'))

    user = get_user(session['username'])
    notes = get_notes(user['id'])

    decrypted_notes = []
    for note in notes:
        decrypted_notes.append({
            "encrypted": note['encrypted_text'],
            "plain": caesar_cipher(note['encrypted_text'], mode='decrypt')
        })

    return render_template("dashboard.html", notes=decrypted_notes)


# -------- ADD NOTE --------
@main.route('/add_note', methods=['GET', 'POST'])
def add_note_view():
    if not require_login():
        return redirect(url_for('main.login'))

    if request.method == "POST":
        text = request.form.get("note_text")
        encrypted = caesar_cipher(text, mode="encrypt")

        user = get_user(session['username'])
        add_note(user['id'], encrypted)

        return redirect(url_for('main.dashboard'))

    return render_template("add_note.html")


# -------- REGISTER --------
@main.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if get_user(username):
            error = "Username taken"
        else:
            password_cipher = caesar_cipher(password, mode="encrypt")
            create_user(username, password_cipher)
            session['username'] = username
            return redirect(url_for('main.dashboard'))

    return render_template("register.html", error=error)


# -------- LOGIN --------
@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if user:
            encrypted_input = caesar_cipher(password, mode="encrypt")
            if encrypted_input == user["password_cipher"]:
                session['username'] = username
                return redirect(url_for('main.dashboard'))

        error = "Invalid credentials"

    return render_template("login.html", error=error)


# -------- LOGOUT --------
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
