import ollama
#change the model as you like 
def ask_llm(prompt: str) -> str:

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

def expand_query(question: str):

    prompt = f"""
You are helping a search engine for RAG.

Given the user's question, generate 5 short search queries that mean the same thing.

Rules:
- Keep each query under 6 words.
- Include synonyms.
- Include important keywords.
- Return ONLY one query per line.

Question:
{question}
"""

    response = ask_llm(prompt)

    queries = []

    for line in response.split("\n"):
        line = line.strip("-•123456789. ").strip()

        if line:
            queries.append(line)

    return list(dict.fromkeys(queries))