import hashlib
from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email, password):
    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, hash_password(password), "staff"),
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE email=?", (email,))
    result = c.fetchone()

    conn.close()

    if result:
        return hash_password(password) == result[0]

    return False
