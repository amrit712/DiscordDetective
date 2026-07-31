from vector_db.chroma_db import search

def retrieve(query: str, n_results: int = 10):

    results = search(query, n_results)

    retrieved = []

    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, distance in zip(documents, metadata, distances):

        retrieved.append({
            "author": meta["author"],
            "channel": meta["channel"],
            "timestamp": meta["timestamp"],
            "content": doc,
            "distance": distance
        })

    return retrieved