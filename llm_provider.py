from ollama import chat


MODEL_NAME = "qwen3:4b"


def generate_structured_response(
    messages: list[dict],
    response_schema: dict,
) -> str:
    """
    Sendet Nachrichten an unser lokales LLM und
    gibt die strukturierte JSON-Antwort als Text zurück.

    Andere Teile unserer Anwendung müssen dadurch
    Ollama nicht direkt aufrufen.
    """

    response = chat(
        model=MODEL_NAME,
        messages=messages,
        format=response_schema,
    )

    return response.message.content