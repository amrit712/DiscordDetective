def build_prompt(question, retrieved_messages):

    context = ""

    for msg in retrieved_messages:

        context += (
            f"[{msg['author']}] "
            f"{msg['content']}\n"
        )

    prompt = f"""
You are an AI that investigates Discord conversations.

Below are Discord messages that were retrieved because they are relevant to the user's question.

Your rules:
1. ONLY use the retrieved messages as evidence.
2. If the answer is uncertain, say so.
3. Quote the messages that support your conclusion.
4. Do NOT invent facts or names.

Retrieved Messages:

{context}

User Question:
{question}

Answer in this format:

Answer:
<your answer>

Evidence:
- "<quoted message>"
- "<quoted message>"
"""

    return prompt