# KI-Agent mit pydantic-ai und langgraph

Dieses Projekt implementiert einen KI-Agenten in Python, der die Frameworks pydantic-ai für Datenvalidierung und langgraph für die Orchestrierung verwendet.

## Überblick

Der KI-Agent kombiniert die Stärken beider Frameworks:

- **pydantic-ai**: Bietet strukturierte Datenvalidierung, Typsicherheit und nahtlose Integration mit LLMs
- **langgraph**: Ermöglicht die Orchestrierung des Agenten-Workflows und zustandsbasierte Verarbeitung

Die Architektur ist modular aufgebaut und kann leicht erweitert werden, um verschiedene Anwendungsfälle zu unterstützen.

## Funktionen

- Verarbeitung von Benutzeranfragen mit strukturierter Ein- und Ausgabe
- Zustandsbasierte Workflow-Orchestrierung
- Integrierte Tools für Suche und Berechnungen
- Konversationsgedächtnis für kontextbezogene Antworten
- Umfassende Testabdeckung

## Installation

### Voraussetzungen

- Python 3.10 oder höher
- pip (Python-Paketmanager)

### Installationsschritte

1. Repository klonen oder Dateien herunterladen

2. Abhängigkeiten installieren:

```bash
pip install pydantic pydantic-ai langgraph
```

## Projektstruktur

```
ai_agent_project/
├── models.py           # Pydantic-Datenmodelle
├── orchestration.py    # Langgraph-Workflow und Orchestrierung
├── agent.py            # Hauptagent-Klasse und Integration
├── test_agent.py       # Unittests
├── architecture.md     # Detaillierte Architekturbeschreibung
└── README.md           # Diese Datei
```

## Verwendung

### Einfaches Beispiel

```python
import asyncio
from agent import KIAgent

async def main():
    # Erstelle den Agenten
    agent = KIAgent()
    
    # Verarbeite eine Anfrage
    response = await agent.process_query("Wie ist das Wetter heute?")
    
    # Gib die Antwort aus
    print(f"Antwort: {response.response}")
    print(f"Konfidenz: {response.confidence}")
    if response.sources:
        print(f"Quellen: {', '.join(response.sources)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Mit Kontext

```python
import asyncio
from agent import KIAgent

async def main():
    # Erstelle den Agenten
    agent = KIAgent()
    
    # Verarbeite eine Anfrage mit zusätzlichem Kontext
    response = await agent.process_query(
        "Wie ist das Wetter heute?",
        context={"location": "Berlin", "user_preference": "Celsius"}
    )
    
    # Gib die Antwort aus
    print(f"Antwort: {response.response}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Architektur

Die Architektur des Agenten besteht aus drei Hauptkomponenten:

1. **Datenmodelle (models.py)**: Definieren die Struktur der Ein- und Ausgabedaten sowie den internen Zustand des Agenten.

2. **Workflow-Orchestrierung (orchestration.py)**: Implementiert den Workflow-Graphen mit langgraph, der den Ablauf der Verarbeitung und die Zustandsübergänge definiert.

3. **Agent-Klasse (agent.py)**: Integriert pydantic-ai und langgraph zu einem vollständigen KI-Agenten mit Tools und Systemkontext.

Für eine detaillierte Beschreibung der Architektur siehe [architecture.md](architecture.md).

## Erweiterung

Der Agent kann auf verschiedene Weise erweitert werden:

### Neue Tools hinzufügen

Fügen Sie neue Methoden zur `KIAgent`-Klasse hinzu:

```python
async def new_tool(self, ctx: RunContext[AgentState], param1: str, param2: int) -> str:
    """
    Beschreibung des neuen Tools.
    
    Args:
        ctx: Der Kontext des pydantic-ai Agenten
        param1: Erster Parameter
        param2: Zweiter Parameter
        
    Returns:
        Das Ergebnis des Tool-Aufrufs
    """
    # Implementierung des Tools
    return f"Ergebnis mit {param1} und {param2}"
```

### Workflow anpassen

Ändern Sie den Workflow-Graphen in `orchestration.py`, um zusätzliche Knoten oder bedingte Verzweigungen hinzuzufügen:

```python
# Neuen Knoten hinzufügen
workflow.add_node("new_node", new_node_function)

# Neue Kante hinzufügen
workflow.add_edge("existing_node", "new_node")
```

## Tests

Das Projekt enthält umfassende Unittests für alle Komponenten. Um die Tests auszuführen:

```bash
python -m unittest test_agent.py
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die LICENSE-Datei für Details.


Ist das markdown ? Und wenn ja, kann markdown python code darstellen, indem man ```python ein gibt ? 
