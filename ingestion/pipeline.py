from database.database import save_message, message_exists
from vector_db.chroma_db import add_message


def ingest_message(message):
    """
    Process a single Discord message.

    Returns:
        True  -> message was indexed
        False -> skipped
    """

    if message.author.bot:
        return False

    if not message.content.strip():
        return False

    if message_exists(message.id):
        return False

    save_message(message)

    add_message(message)

    return True