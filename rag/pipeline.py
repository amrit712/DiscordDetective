from rag.query_expander import expand_query
from retrieval.retriever import retrieve
from rag.prompt_builder import build_prompt
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


def answer(question: str):
    
    queries = expand_query(question)

    all_results = []

    for q in queries:
        results = retrieve(q, n_results=3)
    all_results.extend(results)
    unique = {}

    for msg in all_results:
        unique[msg["content"]] = msg

    messages = list(unique.values())
    messages.sort(key=lambda x: x["distance"])

    if not messages:
        return "I couldn't find anything relevant."

    prompt = build_prompt(question, messages)
    print(prompt)
    response = ask_llm(prompt)

    return response