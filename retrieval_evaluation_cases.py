retrieval_evaluation_cases = [
    {
        "query": (
            "Mein Fahrrad wurde vor dem Bahnhof gestohlen. "
            "Es war mit einem Schloss abgeschlossen."
        ),
        "expected_section": "FAHRRADDIEBSTAHL",
    },
    {
        "query": (
            "Mein Laptop ist heruntergefallen und "
            "das Display ist zerbrochen."
        ),
        "expected_section": "ELEKTRONIKSCHÄDEN",
    },
    {
        "query": (
            "Nach dem Sturm wurden mehrere Dachplatten "
            "meines Hauses beschädigt."
        ),
        "expected_section": "STURMSCHÄDEN",
    },
    {
        "query": (
            "Mein Rucksack wurde aus meinem "
            "abgeschlossenen Auto gestohlen."
        ),
        "expected_section": "DIEBSTAHL AUS FAHRZEUGEN",
    },
        {
        "query": "Mein Hund muss wegen einer Krankheit zum Tierarzt.",
        "expected_section": None,
    },
    {
        "query": "Meine Brille ist beim Sport kaputt gegangen.",
        "expected_section": None,
    },
]