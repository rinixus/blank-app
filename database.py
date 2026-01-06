import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "mixmovie.db"

def init_db():
    """Initializes the database with necessary tables."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Users table (Stores Google User Info)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT
        )
    ''')

    # Movies table
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            title TEXT,
            genre TEXT,
            style TEXT,
            year TEXT,
            file_path TEXT,
            is_public BOOLEAN DEFAULT 0,
            created_at DATETIME,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(email, name):
    """Adds a user if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (email, name) VALUES (?, ?)', (email, name))
    conn.commit()
    conn.close()

def add_movie(user_email, title, genre, style, year, file_path):
    """Adds a new movie entry."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    created_at = datetime.now()
    c.execute('''
        INSERT INTO movies (user_email, title, genre, style, year, file_path, is_public, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, ?)
    ''', (user_email, title, genre, style, year, file_path, created_at))
    conn.commit()
    conn.close()

def get_public_movies():
    """Returns a DataFrame of public movies."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM movies WHERE is_public = 1 ORDER BY created_at DESC", conn)
    conn.close()
    return df

def get_user_movies(user_email):
    """Returns a DataFrame of a specific user's movies."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM movies WHERE user_email = ? ORDER BY created_at DESC", conn, params=(user_email,))
    conn.close()
    return df

def toggle_visibility(movie_id, current_status):
    """Toggles the public/private status of a movie."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    new_status = not current_status
    c.execute("UPDATE movies SET is_public = ? WHERE id = ?", (new_status, movie_id))
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()
