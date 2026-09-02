import sqlite3

import sqlite_vec
from ollama import embed


DB_FILE = "claim_analyzer.db"
EMBEDDING_MODEL = "nomic-embed-text"

# Vorläufiger Testwert aus unserer Retrieval-Evaluation.
# Kleinere Distanz = ähnlicher.
RELEVANCE_THRESHOLD = 0.866


def find_relevant_sections(query: str, top_k: int = 3) -> list[str]:
    """
    Findet die ähnlichsten Versicherungsabschnitte
    mithilfe von Vector Search.

    Wenn der beste Treffer nicht relevant genug ist,
    wird eine leere Liste zurückgegeben.
    """

    response = embed(
        model=EMBEDDING_MODEL,
        input=query,
    )

    query_vector = response["embeddings"][0]
    query_vector_blob = sqlite_vec.serialize_float32(query_vector)

    db = sqlite3.connect(DB_FILE)

    db.enable_load_extension(True)
    sqlite_vec.load(db)

    results = db.execute(
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

    # Falls die Datenbank gar keine Treffer liefert.
    if not results:
        db.close()
        return []

    # Der erste Treffer hat die kleinste Distanz.
    best_distance = results[0][1]

    # Wenn selbst der beste Treffer zu weit entfernt ist,
    # behandeln wir die Anfrage als nicht relevant.
    if best_distance > RELEVANCE_THRESHOLD:
        print(
            f"Kein relevanter Chunk gefunden. "
            f"Beste Distanz: {best_distance:.4f}"
        )

        db.close()
        return []

    relevant_sections = []

    for chunk_id, distance in results:
        chunk = db.execute(
            """
            SELECT section, chunk_text
            FROM chunks
            WHERE id = ?
            """,
            (chunk_id,),
        ).fetchone()

        if chunk is not None:
            section_name, chunk_text = chunk

            print(
                f"Treffer: {section_name} | "
                f"Distanz: {distance}"
            )

            relevant_sections.append(chunk_text)

    db.close()

    return relevant_sections