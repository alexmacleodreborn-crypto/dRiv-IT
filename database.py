import sqlite3

DB_NAME = "drivit.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_tables():
    conn = get_connection()
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT,
        name TEXT,
        mobile TEXT,
        company_id INTEGER
    )
    """)

    # COMPANIES (NEXT STEP READY)
    c.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        landline TEXT,
        logo TEXT
    )
    """)

    conn.commit()
    conn.close()
