import sqlite3

import sqlite_vec
from ollama import embed

from retrieval_evaluation_cases import retrieval_evaluation_cases


DB_FILE = "claim_analyzer.db"
EMBEDDING_MODEL = "nomic-embed-text"

# Testwert für unsere Relevanz-Grenze.
# Kleinere Distanz = ähnlicher.
# Dieser Wert ist noch NICHT als endgültiger Threshold festgelegt.
RELEVANCE_THRESHOLD = 0.866


def retrieve_ranked_sections(query: str, top_k: int = 3):
    """
    Gibt die ähnlichsten Versicherungsabschnitte
    zusammen mit ihrer Distanz zurück.
    """

    # Anfrage in einen Vector umwandeln.
    response = embed(
        model=EMBEDDING_MODEL,
        input=query,
    )

    query_vector = response["embeddings"][0]
    query_vector_blob = sqlite_vec.serialize_float32(query_vector)

    # Vector-Datenbank öffnen.
    db = sqlite3.connect(DB_FILE)

    db.enable_load_extension(True)
    sqlite_vec.load(db)

    # Die top_k ähnlichsten Vectoren suchen.
    vector_results = db.execute(
        """
        SELECT rowid, distance
        FROM chunk_vectors
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT ?
        """,
        (
            query_vector_blob,
            top_k,
        ),
    ).fetchall()

    results = []

    # Aus den Vector-IDs wieder die lesbaren Abschnittsnamen holen.
    for chunk_id, distance in vector_results:
        section = db.execute(
            """
            SELECT section
            FROM chunks
            WHERE id = ?
            """,
            (chunk_id,),
        ).fetchone()

        if section is not None:
            results.append(
                {
                    "section": section[0],
                    "distance": distance,
                }
            )

    db.close()

    return results


# Zähler für unsere Evaluation.
top1_correct = 0
top3_correct = 0
relevant_cases = 0
relevance_correct = 0


for case in retrieval_evaluation_cases:
    query = case["query"]
    expected = case["expected_section"]

    results = retrieve_ranked_sections(
        query,
        top_k=3,
    )

    # Prüfen, ob der beste Treffer unter
    # unserer aktuellen Relevanz-Grenze liegt.
    if results:
        best_distance = results[0]["distance"]

        if best_distance <= RELEVANCE_THRESHOLD:
            predicted_relevant = True
        else:
            predicted_relevant = False
    else:
        predicted_relevant = False

    # Wenn expected nicht None ist, erwarten wir,
    # dass relevantes Wissen vorhanden ist.
    expected_relevant = expected is not None

    # War unsere Relevanz-Entscheidung richtig?
    if predicted_relevant == expected_relevant:
        relevance_correct += 1

    print(f"Anfrage:  {query}")
    print(f"Erwartet: {expected}")
    print(f"Als relevant erkannt: {predicted_relevant}")
    print()

    # Ranking der gefundenen Chunks ausgeben.
    for position, result in enumerate(results, start=1):
        print(
            f"{position}. {result['section']} "
            f"(Distanz: {result['distance']:.4f})"
        )

    # Nur die Abschnittsnamen aus den Ergebnissen holen.
    found_sections = [
        result["section"]
        for result in results
    ]

    # Top-1 und Top-3 bewerten wir nur,
    # wenn tatsächlich ein passender Chunk existieren soll.
    if expected is not None:
        relevant_cases += 1

        # Ist der richtige Chunk direkt auf Platz 1?
        if results and results[0]["section"] == expected:
            top1_correct += 1

        # Ist der richtige Chunk wenigstens unter den Top 3?
        if expected in found_sections:
            top3_correct += 1

    print()


# Gesamtergebnisse berechnen.
total = len(retrieval_evaluation_cases)

top1_accuracy = top1_correct / relevant_cases * 100
top3_hit_rate = top3_correct / relevant_cases * 100
relevance_accuracy = relevance_correct / total * 100


print("--------------------")
print(f"Testfälle: {total}")

print(
    f"Top-1 Accuracy: "
    f"{top1_correct}/{relevant_cases} "
    f"({top1_accuracy:.1f} %)"
)

print(
    f"Top-3 Hit Rate: "
    f"{top3_correct}/{relevant_cases} "
    f"({top3_hit_rate:.1f} %)"
)

print(
    f"Relevance Accuracy: "
    f"{relevance_correct}/{total} "
    f"({relevance_accuracy:.1f} %)"
)