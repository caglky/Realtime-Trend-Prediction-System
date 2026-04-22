import sqlite3
import os 

def create_connection(db_path = "database/trends.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn

def create_table():
    conn = create_connection() 
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT, 
                   word TEXT, 
                   today_count INTEGER,
                   yesterday_count INTEGER,
                   growth_rate REAL,
                   trend_score REAL,
                   label INTEGER)
                   """)
    conn.commit()
    conn.close()

def insert_trend_rows (rows, date_str):
    conn = create_connection()
    cursor = conn.cursor()
    for row in rows:
        cursor.execute("""
        INSERT INTO trends (
                       date, word, today_count, 
                       yesterday_count, growth_rate, trend_score, label)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """ ,(
                           date_str,
                           row["word"],
                           row["today_count"], 
                           row["yesterday_count "],
                           row["growth_rate"],
                           row["trend_score"],
                           row["label"]
                       ))
    conn.commit()
    conn.close()

def fetch_all_trend():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trends")
    rows = cursor.fetchall()
    conn.close()
    return rows