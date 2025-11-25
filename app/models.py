import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

# -------- USERS --------

def create_user(username, password_cipher):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_cipher) VALUES (%s, %s)",
                (username, password_cipher))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    conn.close()
    return user

# -------- NOTES --------

def add_note(user_id, encrypted_text):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (user_id, encrypted_text) VALUES (%s, %s)",
                (user_id, encrypted_text))
    conn.commit()
    conn.close()

def get_notes(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM notes WHERE user_id = %s ORDER BY id DESC", (user_id,))
    notes = cur.fetchall()
    conn.close()
    return notes
