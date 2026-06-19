import sqlite3
from datetime import datetime

DB_NAME="Weather_API.db"

def get_connection():
        conn = sqlite3.connect(DB_NAME)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id    TEXT PRIMARY KEY,
    email   TEXT UNIQUE NOT NULL,
    password   TEXT NOT NULL,
    name       TEXT NOT NULL,
    created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favoritecity (
        id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,
    city        TEXT NOT NULL,
    added_at  TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
                   )
            """)
    
    conn.commit()
    conn.close()

def save_user(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, email, password, name, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user.user_id, user.email, user.password, user.name, user.created_at))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "email": row[1],
            "password": row[2],
            "name": row[3],
            "created_at": row[4]
        }
    return None

def user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "email": row[1],
            "password": row[2],
            "name": row[3],
            "created_at": row[4]
        }
    return None

def save_favorite_city(favorite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO favoritecity(id, user_id, city, added_at)
        VALUES (?, ?, ?, ?)
    """, (favorite.id, favorite.user_id, favorite.city, favorite.added_at))

    conn.commit()
    conn.close()

def get_favorites_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favoritecity WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    favoritecity = []
    for row in rows:
        favoritecity.append({
            "id": row[0],
            "user_id": row[1],
            "city": row[2],
            "added_at": row[3]
        })
    return favoritecity

def delete_favorite(user_id, city):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favoritecity WHERE user_id = ? AND city = ?", (user_id, city))
    deleted = cursor.rowcount > 0   # True if 1+ rows were deleted, False if none matched
    conn.commit()
    conn.close()
    return deleted

