import pytest
from unittest.mock import patch

from analyzer import analyze_claim
from llm_classifier import ClaimClassification
from pydantic import ValidationError

from models import Claim


def test_valid_claim():
    claim = Claim(
        contract_number="V-12345",
        description="Mein Fahrrad wurde gestohlen.",
        police_reported=True,
    )

    assert claim.contract_number == "V-12345"
    assert claim.description == "Mein Fahrrad wurde gestohlen."
    assert claim.police_reported is True


def test_contract_number_too_short():
    with pytest.raises(ValidationError):
        Claim(
            contract_number="12",
            description="Mein Fahrrad wurde gestohlen.",
            police_reported=True,
        )


def test_description_too_short():
    with pytest.raises(ValidationError):
        Claim(
            contract_number="V-12345",
            description="zu kurz",
            police_reported=True,
        )


def test_invalid_police_reported():
    with pytest.raises(ValidationError):
        Claim(
            contract_number="V-12345",
            description="Mein Fahrrad wurde gestohlen.",
            police_reported="Banane",
        )


def test_analyze_claim_with_mocked_llm():
    claim = Claim(
        contract_number="V-12345",
        description="Jemand hat mein Fahrrad mitgenommen.",
        police_reported=True,
    )

    fake_classification = ClaimClassification(
        category="Diebstahl"
    )

    # Während dieses Tests soll analyzer.py nicht
    # die echte classify_claim()-Funktion verwenden.
    with patch(
        "analyzer.classify_claim",
        return_value=fake_classification,
    ):
        analysis = analyze_claim(claim)

    assert analysis.category == "Diebstahl"
    assert analysis.police_status == "Polizei wurde informiert."


def test_rag_without_relevant_knowledge_does_not_call_llm(monkeypatch):
    from rag_service import answer_claim_question

    # Wir simulieren, dass der Retriever nichts Relevantes findet.
    monkeypatch.setattr(
        "rag_service.find_relevant_sections",
        lambda description, top_k=3: [],
    )

    # Wenn die LLM-Funktion trotzdem aufgerufen wird,
    # soll der Test sofort fehlschlagen.
    def fake_generate(*args, **kwargs):
        raise AssertionError(
            "Das LLM darf ohne relevante Chunks nicht aufgerufen werden."
        )

    monkeypatch.setattr(
        "rag_service.generate_structured_response",
        fake_generate,
    )

    result = answer_claim_question(
        "Mein Hund muss wegen einer Krankheit zum Tierarzt."
    )

    assert result.coverage_status == "unklar"
    assert result.missing_information == [
        "Für diesen Schadenfall sind keine passenden "
        "Versicherungsbedingungen vorhanden."
    ]


def test_rag_with_relevant_knowledge_calls_llm(monkeypatch):
    from rag_service import answer_claim_question

    # Wir simulieren, dass der Retriever
    # einen passenden Chunk findet.
    monkeypatch.setattr(
        "rag_service.find_relevant_sections",
        lambda description, top_k=3: [
            (
                "FAHRRADDIEBSTAHL\n\n"
                "Der Diebstahl eines Fahrrads ist versichert, "
                "wenn das Fahrrad mit einem geeigneten Schloss gesichert war."
            )
        ],
    )

    # Wir simulieren die JSON-Antwort,
    # die normalerweise vom LLM-Provider kommt.
    def fake_generate(*args, **kwargs):
        return (
            '{"coverage_status":"potenziell_gedeckt",'
            '"reason":"Das Fahrrad war mit einem geeigneten Schloss gesichert.",'
            '"missing_information":[]}'
        )

    monkeypatch.setattr(
        "rag_service.generate_structured_response",
        fake_generate,
    )

    result = answer_claim_question(
        "Mein Fahrrad wurde gestohlen. "
        "Es war mit einem geeigneten Schloss abgeschlossen."
    )

    assert result.coverage_status == "potenziell_gedeckt"
    assert result.missing_information == []
    assert "geeigneten Schloss" in result.reason