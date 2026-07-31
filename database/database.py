import sqlite3

conn = sqlite3.connect("discord.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY,
    author TEXT,
    author_id TEXT,
    channel TEXT,
    guild TEXT,
    timestamp TEXT,
    content TEXT,
    reply_to TEXT,
    edited BOOLEAN,
    deleted BOOLEAN,
    attachments TEXT,
    jump_url TEXT,
    embedding TEXT
)
""")
def message_exists(message_id):
    cursor.execute(
        "SELECT 1 FROM messages WHERE id = ?",
        (message_id,)
    )
    return cursor.fetchone() is not None
def save_message(message):

    cursor.execute("""
    INSERT INTO messages
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        message.id,
        str(message.author),
        str(message.author.id),
        str(message.channel),
        str(message.guild),
        str(message.created_at),
        message.content,
        None,  # reply_to
        False,  # edited
        False,  # deleted
        None,  # attachments
        None,   # jump_url
        None   # embedding
    ))

    conn.commit()