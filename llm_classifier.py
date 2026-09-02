from typing import Literal

from pydantic import BaseModel

from llm_provider import generate_structured_response


class ClaimClassification(BaseModel):
    category: Literal["Diebstahl", "Sachschaden", "Unbekannt"]


class LLMServiceError(Exception):
    pass


def classify_claim(description: str) -> ClaimClassification:
    try:
        content = generate_structured_response(
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
                    ),
                },
                {
                    "role": "user",
                    "content": description,
                },
            ],
            response_schema=ClaimClassification.model_json_schema(),
        )

        return ClaimClassification.model_validate_json(content)

    except Exception as error:
        raise LLMServiceError(
            "Die Schadenklassifizierung ist fehlgeschlagen."
        ) from error