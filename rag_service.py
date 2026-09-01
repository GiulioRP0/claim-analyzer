from ollama import chat

from rag_retriever import find_relevant_section


def answer_claim_question(description: str) -> str:
    """
    Beantwortet eine Schadenfrage mithilfe unseres Versicherungswissens.

    Ablauf:
    1. Passenden Abschnitt aus den Versicherungsbedingungen finden.
    2. Diesen Abschnitt zusammen mit der Schadenbeschreibung an Qwen senden.
    3. Qwens Antwort zurückgeben.
    """

    # Das ist das "Retrieval":
    # Wir suchen zuerst relevantes Wissen aus unserer eigenen Datei.
    context = find_relevant_section(description)

    # Jetzt kommt "Augmented Generation":
    # Qwen bekommt nicht nur die Schadenbeschreibung,
    # sondern zusätzlich den gefundenen Versicherungs-Kontext.
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein Assistent für Versicherungsschäden. "
                    "Beantworte die Frage ausschließlich anhand der "
                    "bereitgestellten Versicherungsbedingungen. "
                    "Wenn die Informationen nicht ausreichen, sage das klar. "
                    "Erfinde keine Versicherungsbedingungen."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Schadenbeschreibung:\n{description}\n\n"
                    f"Relevante Versicherungsbedingungen:\n{context}\n\n"
                    "Beurteile anhand dieser Informationen, "
                    "ob der Schaden grundsätzlich versichert sein könnte."
                ),
            },
        ],
    )

    return response.message.content