from models import CoverageAssessment
from rag_retriever import find_relevant_sections
from llm_provider import generate_structured_response


def answer_claim_question(description: str) -> CoverageAssessment:
    """
    Beurteilt einen Schaden anhand der gefundenen Versicherungsbedingungen.

    Wenn keine relevanten Bedingungen gefunden werden,
    wird direkt ein unklarer Status zurückgegeben.
    """

    sections = find_relevant_sections(
        description,
        top_k=3,
    )

    # Wenn unser Retriever keine relevanten Chunks findet,
    # soll das LLM nicht raten.
    if not sections:
        return CoverageAssessment(
            coverage_status="unklar",
            reason=(
                "In den verfügbaren Versicherungsbedingungen wurde "
                "kein relevanter Abschnitt gefunden."
            ),
            missing_information=[
                "Für diesen Schadenfall sind keine passenden "
                "Versicherungsbedingungen vorhanden."
            ],
        )

    context = "\n\n---\n\n".join(sections)

    content = generate_structured_response(
        messages=[
            {
                "role": "system",
                "content": (
                    "Du beurteilst Versicherungsschäden ausschließlich anhand "
                    "der bereitgestellten Versicherungsbedingungen. "

                    "Verwende 'potenziell_gedeckt', wenn die bekannten "
                    "Informationen grundsätzlich für eine Deckung sprechen. "

                    "Verwende 'nicht_gedeckt', wenn aus den Bedingungen klar "
                    "hervorgeht, dass der Schaden nicht gedeckt ist. "

                    "Verwende 'unklar', wenn wichtige Informationen fehlen, "
                    "um die Deckung sicher beurteilen zu können. "

                    "Trage fehlende Informationen in missing_information ein. "
                    "Erfinde keine fehlenden Informationen."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Schadenbeschreibung:\n{description}\n\n"
                    f"Versicherungsbedingungen:\n{context}"
                ),
            },
        ],
        response_schema=CoverageAssessment.model_json_schema(),
    )

    return CoverageAssessment.model_validate_json(content)