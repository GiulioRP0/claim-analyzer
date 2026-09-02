from pathlib import Path
import sqlite3

import sqlite_vec
from ollama import embed


DB_FILE = "claim_analyzer.db"
KNOWLEDGE_FILE = Path("knowledge/insurance_conditions.txt")
EMBEDDING_MODEL = "nomic-embed-text"


def load_sections() -> list[str]:
    """Liest die Versicherungsbedingungen und teilt sie in Abschnitte."""

    knowledge = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    sections = knowledge.split("\n\n\n")

    return sections


def save_sections() -> None:
    """Speichert Text-Chunks und ihre Embeddings in SQLite."""

    sections = load_sections()

    db = sqlite3.connect(DB_FILE)

    # sqlite-vec für diese Datenbankverbindung aktivieren.
    db.enable_load_extension(True)
    sqlite_vec.load(db)

    # Alte Daten löschen, damit beim erneuten Ausführen
    # keine doppelten Chunks und Vektoren entstehen.
    db.execute("DELETE FROM chunk_vectors")
    db.execute("DELETE FROM chunks")

    for section in sections:
        lines = section.strip().splitlines()

        section_name = lines[0]
        chunk_text = section.strip()

        # Zuerst speichern wir den lesbaren Text.
        cursor = db.execute(
            """
            INSERT INTO chunks (source, section, chunk_text)
            VALUES (?, ?, ?)
            """,
            (
                "insurance_conditions.txt",
                section_name,
                chunk_text,
            ),
        )

        # SQLite gibt uns die ID des gerade gespeicherten Chunks.
        chunk_id = cursor.lastrowid

        # Jetzt wandeln wir den Chunk in ein Embedding um.
        response = embed(
            model=EMBEDDING_MODEL,
            input=chunk_text,
        )

        vector = response["embeddings"][0]

        # Der Vector wird als Binärdaten für sqlite-vec vorbereitet.
        vector_blob = sqlite_vec.serialize_float32(vector)

        # rowid entspricht der ID aus unserer normalen chunks-Tabelle.
        db.execute(
            """
            INSERT INTO chunk_vectors (rowid, embedding)
            VALUES (?, ?)
            """,
            (
                chunk_id,
                vector_blob,
            ),
        )

        print(f"Gespeichert: {section_name}")

    db.commit()
    db.close()

    print(f"{len(sections)} Chunks und Embeddings wurden gespeichert.")


if __name__ == "__main__":
    save_sections()