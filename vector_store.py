import sqlite3

import sqlite_vec


DB_FILE = "claim_analyzer.db"


def create_database() -> None:
    """Erstellt unsere lokale Datenbank und die benötigten Tabellen."""

    # SQLite öffnet die Datei.
    # Falls claim_analyzer.db noch nicht existiert,
    # wird sie automatisch erstellt.
    db = sqlite3.connect(DB_FILE)

    # sqlite-vec erweitert diese SQLite-Verbindung
    # um Funktionen für unsere Vector Search.
    db.enable_load_extension(True)
    sqlite_vec.load(db)

    # NORMALE TABELLE:
    # Hier speichern wir später den lesbaren Text
    # und Informationen darüber, woher der Text kommt.
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            section TEXT NOT NULL,
            chunk_text TEXT NOT NULL
        )
        """
    )

    # VECTOR-TABELLE:
    # Diese virtuelle Tabelle wird von sqlite-vec verwaltet.
    # Hier speichern wir später die 768-dimensionalen Embeddings.
    db.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunk_vectors
        USING vec0(
            embedding FLOAT[768]
        )
        """
    )

    # Änderungen dauerhaft in die DB schreiben.
    db.commit()

    # Verbindung wieder schließen.
    db.close()

    print("Vector-Datenbank wurde vorbereitet.")


if __name__ == "__main__":
    create_database()