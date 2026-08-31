from typing import Literal

from ollama import chat
from pydantic import BaseModel


class ClaimClassification(BaseModel):
    category: Literal["Diebstahl", "Sachschaden", "Unbekannt"]


class LLMServiceError(Exception):
    pass


def classify_claim(description: str) -> ClaimClassification:
    try:
        response = chat(
            model="qwen3:4b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du klassifizierst Versicherungsschäden. "
                        "Erlaubte Kategorien sind ausschließlich: "
                        "Diebstahl, Sachschaden oder Unbekannt."
                    )
                },
                {
                    "role": "user",
                    "content": description
                }
            ],
            format=ClaimClassification.model_json_schema()
        )

        return ClaimClassification.model_validate_json(
            response.message.content
        )

    except Exception as error:
        raise LLMServiceError(
            "Die Schadenklassifizierung ist fehlgeschlagen."
        ) from error