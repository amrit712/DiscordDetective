import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_data")

collection = client.get_or_create_collection(
    name="discord_messages"
)
#change the model to any other model from https://huggingface.co/sentence-transformers
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
def get_embedding(text: str):
    return model.encode(text)

def add_message(message):

    if not message.content.strip():
        return

    embedding = get_embedding(message.content)

    collection.upsert(
        ids=[str(message.id)],
        embeddings=[embedding.tolist()],
        documents=[message.content],
        metadatas=[{
            "author": str(message.author),
            "author_id": str(message.author.id),
            "channel": str(message.channel),
            "guild": str(message.guild),
            "timestamp": str(message.created_at)
        }]
    )


def search(query: str, n_results: int = 5):

    embedding = get_embedding(query)

    return collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )