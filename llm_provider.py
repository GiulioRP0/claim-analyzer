import os

from ollama import Client


MODEL_NAME = "qwen3:4b"

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

client = Client(
    host=OLLAMA_HOST,
)


def generate_structured_response(
    messages: list[dict],
    response_schema: dict,
) -> str:
    """
    Sendet Nachrichten an unser lokales LLM und
    gibt die strukturierte JSON-Antwort als Text zurück.

    Der Ollama-Host kann über die Umgebungsvariable
    OLLAMA_HOST konfiguriert werden.
    """

    response = client.chat(
        model=MODEL_NAME,
        messages=messages,
        format=response_schema,
    )

    return response.message.content