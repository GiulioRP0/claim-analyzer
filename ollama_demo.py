from typing import Literal

from ollama import chat
from pydantic import BaseModel


class ClaimClassification(BaseModel):
    category: Literal["Diebstahl", "Sachschaden", "Unbekannt"]

response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "system",
            "content": (
                "Du klassifizierst Versicherungsschäden. "
                "Erlaubte Kategorien sind: "
                "Diebstahl, Sachschaden oder Unbekannt."
            )
        },
        {
            "role": "user",
            "content": (
                "Jemand hat mein Fahrrad mitgenommen, "
                "während ich im Laden war."
            )
        }
    ],
    format=ClaimClassification.model_json_schema()
)

classification = ClaimClassification.model_validate_json(
    response.message.content
)

print(classification)
print(classification.category)