from pathlib import Path


KNOWLEDGE_FILE = Path("knowledge/insurance_conditions.txt")


def load_knowledge() -> str:
    return KNOWLEDGE_FILE.read_text(encoding="utf-8")


def find_relevant_section(query: str) -> str:
    knowledge = load_knowledge()

    sections = knowledge.split("\n\n\n")

    query_lower = query.lower()

    for section in sections:
        section_lower = section.lower()

        if "fahrrad" in query_lower and "fahrraddiebstahl" in section_lower:
            return section

        if (
            any(word in query_lower for word in ["handy", "tablet", "laptop", "fernseher"])
            and "elektronikschäden" in section_lower
        ):
            return section

        if "sturm" in query_lower and "sturmschäden" in section_lower:
            return section

        if (
            any(word in query_lower for word in ["auto", "fahrzeug", "rucksack"])
            and "diebstahl aus fahrzeugen" in section_lower
        ):
            return section

    return "Keine passende Versicherungsbedingung gefunden."