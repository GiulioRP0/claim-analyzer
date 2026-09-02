# Claim Analyzer

Der Claim Analyzer ist ein Lern- und Portfolio-Projekt zur Analyse von Versicherungsschäden mit Python und künstlicher Intelligenz.

Das Projekt wurde entwickelt, um praktische Erfahrungen im Bereich AI Software Engineering zu sammeln. Dabei werden klassische Softwareentwicklung, eine REST-API, ein lokales Large Language Model (LLM), RAG, Vector Search, automatisierte Tests und Docker miteinander kombiniert.

## Funktionen

Der Claim Analyzer kann:

- Schadenmeldungen über eine FastAPI-API entgegennehmen
- Schadenbeschreibungen mit einem lokalen LLM klassifizieren
- strukturierte KI-Antworten mit Pydantic validieren
- eigene Versicherungsbedingungen mit RAG einbeziehen
- relevante Versicherungsbedingungen über Vector Search finden
- Embeddings lokal erzeugen
- strukturierte Einschätzungen zur möglichen Versicherungsdeckung erzeugen
- automatisierte Tests ausführen
- als Docker-Container gestartet werden

## Technologien

Im Projekt werden unter anderem folgende Technologien verwendet:

- Python
- FastAPI
- Pydantic
- Ollama
- Qwen
- nomic-embed-text
- SQLite
- sqlite-vec
- pytest
- GitHub Actions
- Docker

## Architektur

Vereinfacht besteht die Anwendung aus folgenden Komponenten:

```text
User
 ↓
FastAPI
 ↓
Analyzer / RAG Service
 ↓
LLM Provider
 ↓
Ollama
 ├── Qwen
 └── nomic-embed-text
          ↓
       sqlite-vec
```

Ollama stellt die lokalen KI-Modelle bereit.

Qwen wird für die Klassifikation und Generierung von Antworten verwendet.

`nomic-embed-text` erzeugt Embeddings, mit denen Texte anhand ihrer Bedeutung verglichen werden können.

SQLite und `sqlite-vec` werden verwendet, um die Versicherungsbedingungen und ihre Vektoren zu speichern und nach relevanten Informationen zu suchen.

## RAG

Das Projekt verwendet Retrieval-Augmented Generation (RAG).

Dadurch kann das LLM bei einer Schadenanalyse eigene Versicherungsbedingungen als zusätzlichen Kontext verwenden.

Vereinfacht funktioniert der Ablauf so:

```text
Versicherungsbedingungen
        ↓
      Chunks
        ↓
    Embeddings
        ↓
      Vektoren
        ↓
    Vector-Datenbank
        ↓
    Vector Search
        ↓
relevante Versicherungsbedingungen
        ↓
       Qwen
        ↓
strukturierte Antwort
```

Die Versicherungsbedingungen werden zunächst in kleinere Textabschnitte (Chunks) aufgeteilt.

Für jeden Chunk wird mit `nomic-embed-text` ein Embedding erzeugt. Dieses repräsentiert die Bedeutung des Textes als Zahlenvektor.

Bei einer neuen Schadenbeschreibung wird ebenfalls ein Embedding erzeugt.

`sqlite-vec` vergleicht anschließend den Vektor der Schadenbeschreibung mit den gespeicherten Vektoren und sucht nach den ähnlichsten Versicherungsbedingungen.

Die gefundenen Textabschnitte werden Qwen als zusätzlicher Kontext übergeben.

Das LLM erzeugt daraus eine strukturierte Einschätzung.

## Strukturierte Antworten

Für die KI-Antworten werden Pydantic-Modelle verwendet.

Eine RAG-Antwort enthält beispielsweise:

```text
coverage_status
reason
missing_information
```

Damit liefert das LLM nicht einfach beliebigen Text zurück, sondern eine vorher definierte Struktur, die von der Anwendung validiert und weiterverarbeitet werden kann.

Mögliche Werte für `coverage_status` sind:

```text
potenziell_gedeckt
nicht_gedeckt
unklar
```

Fehlen wichtige Informationen für eine Einschätzung, sollen diese über `missing_information` angegeben werden.

## Tests und Evaluation

Das Projekt enthält automatisierte Tests mit pytest.

Externe LLM-Aufrufe werden in Unit Tests gemockt. Dadurch können die Tests schnell und unabhängig von einem laufenden Ollama-Modell ausgeführt werden.

Tests können mit folgendem Befehl ausgeführt werden:

```powershell
python -m pytest -v
```

Zusätzlich wurden eigene Evaluationen für die LLM-Klassifikation und das RAG-Retrieval erstellt.

Damit wird nicht nur geprüft, ob der Code technisch funktioniert, sondern auch, wie gut Klassifikation und Retrieval bei vorbereiteten Testfällen funktionieren.

Die Tests werden zusätzlich über GitHub Actions automatisch ausgeführt.

## Projekt lokal starten

### 1. Abhängigkeiten installieren

```powershell
python -m pip install -r requirements.txt
```

### 2. Ollama-Modelle installieren

Für Klassifikation und Generierung wird Qwen verwendet:

```powershell
ollama pull qwen3:4b
```

Für die Embeddings wird `nomic-embed-text` verwendet:

```powershell
ollama pull nomic-embed-text
```

### 3. Vector-Datenbank vorbereiten

Zuerst wird die Datenbankstruktur erstellt:

```powershell
python vector_store.py
```

Danach werden die Versicherungsbedingungen indexiert:

```powershell
python index_knowledge.py
```

Dabei werden die Versicherungsbedingungen eingelesen, in Chunks aufgeteilt, in Embeddings umgewandelt und in der Vector-Datenbank gespeichert.

### 4. FastAPI starten

```powershell
python -m uvicorn api:app --reload
```

Anschließend ist die Swagger-Oberfläche unter folgender Adresse erreichbar:

```text
http://127.0.0.1:8000/docs
```

### 5. Tests ausführen

```powershell
python -m pytest -v
```

## Mit Docker starten

Das Projekt kann auch in einem Docker-Container ausgeführt werden.

### Docker-Image bauen

```powershell
docker build -t claim-analyzer .
```

### Container starten

```powershell
docker run --name claim-analyzer-container -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 claim-analyzer
```

Ollama läuft dabei auf dem Host-System und wird vom Docker-Container über `host.docker.internal` erreicht.

Die Swagger-Oberfläche ist anschließend unter folgender Adresse erreichbar:

```text
http://localhost:8000/docs
```

### RAG-Datenbank im Container vorbereiten

Die Vector-Datenbank wird innerhalb des laufenden Containers erstellt:

```powershell
docker exec claim-analyzer-container python vector_store.py
```

Danach werden die Versicherungsbedingungen indexiert:

```powershell
docker exec claim-analyzer-container python index_knowledge.py
```

Die erzeugte SQLite-Datenbank wird nicht im Git-Repository gespeichert, da sie aus den vorhandenen Versicherungsbedingungen reproduzierbar erstellt werden kann.

## Konfiguration

Die Verbindung zu Ollama kann über die Environment Variable `OLLAMA_HOST` konfiguriert werden.

Standardmäßig verwendet die Anwendung:

```text
http://localhost:11434
```

Beim Betrieb innerhalb von Docker kann beispielsweise verwendet werden:

```text
http://host.docker.internal:11434
```

Dadurch muss die Ollama-Adresse nicht fest an mehreren Stellen im Code eingetragen werden.

## Wichtige Designentscheidungen

### Lokales LLM

Das Projekt verwendet Ollama und Qwen lokal.

Dadurch können die LLM-Aufrufe ohne externe Runtime-API durchgeführt werden. Gleichzeitig eignet sich dieser Ansatz gut, um sich mit Themen wie Datenschutz, lokalen Modellen und On-Premise-Szenarien auseinanderzusetzen.

### Provider-Abstraktion

Der direkte Zugriff auf das LLM wurde von der eigentlichen Anwendungslogik getrennt.

Dadurch kennt beispielsweise die Schadenanalyse nicht alle technischen Details darüber, wie Ollama angesprochen wird.

### Structured Output

LLM-Antworten werden mit Pydantic validiert.

Dadurch kann die Anwendung mit einer definierten Datenstruktur arbeiten, statt sich auf frei formulierte KI-Antworten verlassen zu müssen.

### RAG statt ausschließlich Modellwissen

Versicherungsbedingungen werden nicht als Wissen des LLM vorausgesetzt.

Stattdessen sucht das RAG-System passende Informationen aus den hinterlegten Versicherungsbedingungen und gibt sie dem Modell als Kontext.

## Grenzen des Projekts

Der Claim Analyzer ist ein Lern- und Portfolio-Projekt und keine produktive Versicherungssoftware.

Die verwendeten Versicherungsbedingungen sind Demo-Daten.

Das RAG-System arbeitet aktuell mit einem kleinen Datensatz und einem experimentell bestimmten Relevanz-Threshold.

Auch mit RAG können LLMs falsche oder nicht ausreichend belegte Aussagen erzeugen. Deshalb sind Evaluation, Validierung und weitere Guardrails für produktive Systeme wichtig.

## Mögliche Weiterentwicklung

Mögliche spätere Erweiterungen sind:

- umfangreichere RAG-Evaluation
- größere Wissensbasis
- Vergleich verschiedener LLMs
- Vergleich lokaler und Cloud-basierter Modelle
- weitere Guardrails
- Agent- oder Workflow-basierte Verarbeitung

## Projektstatus

Das Projekt befindet sich in aktiver Entwicklung und dient als praktisches Lern- und Portfolio-Projekt im Bereich AI Software Engineering.