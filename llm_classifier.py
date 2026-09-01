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
                        "Du klassifizierst Versicherungsschäden anhand der Beschreibung. "
                        "Verwende ausschließlich eine dieser Kategorien: "
                        "Diebstahl, Sachschaden oder Unbekannt. "

                        "Definitionen: "
                        "Diebstahl = Ein Gegenstand wurde einer Person unberechtigt weggenommen. "
                        "Sachschaden = Ein Gegenstand wurde durch ein erkennbares äußeres Ereignis beschädigt. "
                        "Unbekannt = Aus der Beschreibung lässt sich Diebstahl oder Sachschaden nicht sicher bestimmen. "

                        "Wenn lediglich beschrieben wird, dass ein Gerät nicht mehr funktioniert, "
                        "aber keine Ursache oder kein äußeres Schadenereignis genannt wird, "
                        "verwende Unbekannt."
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