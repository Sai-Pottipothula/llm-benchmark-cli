import sqlite3
import hashlib
import json

DB_NAME = "cache.db"


def init_cache():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            key TEXT PRIMARY KEY,
            provider TEXT,
            prompt TEXT,
            system TEXT,
            response TEXT
        )
    """)

    conn.commit()
    conn.close()


def make_key(provider, prompt, system):
    raw = f"{provider}:{prompt}:{system}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached_response(provider, prompt, system):
    init_cache()

    key = make_key(provider, prompt, system)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT response FROM responses WHERE key = ?", (key,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return json.loads(row[0])

    return None


def save_cached_response(provider, prompt, system, response):
    init_cache()

    key = make_key(provider, prompt, system)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO responses
        VALUES (?, ?, ?, ?, ?)
    """, (
        key,
        provider,
        prompt,
        system,
        json.dumps(response)
    ))

    conn.commit()
    conn.close()