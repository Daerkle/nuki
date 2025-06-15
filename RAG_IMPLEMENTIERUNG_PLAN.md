# RAG-Implementierungsplan

## Aufgabe
Das DEFAULT_RAG_TEMPLATE und die Standard-Parameter in der `backend/open_webui/config.py` Datei aktualisieren.

## Zu ändernde Parameter

### 1. DEFAULT_RAG_TEMPLATE (Zeile 2221-2249)
**Ersetzen durch:**
```python
DEFAULT_RAG_TEMPLATE = """Generate Response to User Query  
Step 1: Parse Context Information  
Extract and utilize relevant knowledge from the provided context within <context></context> XML tags.  

Step 2: Analyze User Query  
Carefully read and comprehend the user's query, pinpointing the key concepts, entities, and intent behind the question.  

Step 3: Determine Response  
If the answer to the user's query can be directly inferred from the context information, provide a concise and accurate response in the same language as the user's query.  

Step 4: Handle Uncertainty  
If the answer is not clear, ask the user for clarification to ensure an accurate response.  

Step 5: Avoid Context Attribution  
When formulating your response, do not indicate that the information was derived from the context.  

Step 6: Respond in User's Language  
Maintain consistency by ensuring the response is in the same language as the user's query.  

Step 7: Provide Response  
Generate a clear, concise, and informative response to the user's query, adhering to the guidelines outlined above.  

User Query: {{QUERY}}  
<context>{{CONTEXT}}</context>"""
```

### 2. RAG_TOP_K (Zeile 2054-2056)
**Ändern von:**
```python
RAG_TOP_K = PersistentConfig(
    "RAG_TOP_K", "rag.top_k", int(os.environ.get("RAG_TOP_K", "3"))
)
```
**Zu:**
```python
RAG_TOP_K = PersistentConfig(
    "RAG_TOP_K", "rag.top_k", int(os.environ.get("RAG_TOP_K", "10"))
)
```

### 3. CHUNK_SIZE (Zeile 2212-2214)
**Ändern von:**
```python
CHUNK_SIZE = PersistentConfig(
    "CHUNK_SIZE", "rag.chunk_size", int(os.environ.get("CHUNK_SIZE", "1000"))
)
```
**Zu:**
```python
CHUNK_SIZE = PersistentConfig(
    "CHUNK_SIZE", "rag.chunk_size", int(os.environ.get("CHUNK_SIZE", "2000"))
)
```

### 4. CHUNK_OVERLAP (Zeile 2215-2219)
**Ändern von:**
```python
CHUNK_OVERLAP = PersistentConfig(
    "CHUNK_OVERLAP",
    "rag.chunk_overlap",
    int(os.environ.get("CHUNK_OVERLAP", "100")),
)
```
**Zu:**
```python
CHUNK_OVERLAP = PersistentConfig(
    "CHUNK_OVERLAP",
    "rag.chunk_overlap",
    int(os.environ.get("CHUNK_OVERLAP", "500")),
)
```

## Implementierungsschritte

1. **Template-Aktualisierung**: Das DEFAULT_RAG_TEMPLATE vollständig ersetzen
2. **Parameter-Anpassung**: Die drei Standard-Werte für TOP_K, CHUNK_SIZE und CHUNK_OVERLAP ändern
3. **Platzhalter-Konsistenz**: Sicherstellen, dass {{QUERY}} und {{CONTEXT}} korrekt verwendet werden
4. **Validierung**: Überprüfen, dass alle Änderungen syntaktisch korrekt sind

## Wichtige Punkte

- Die Platzhalter {{QUERY}} und {{CONTEXT}} müssen beibehalten werden, da sie vom System erwartet werden
- Das neue Template behält die XML-Struktur bei (`<context></context>`)
- Die Standard-Werte ändern sich nur für neue Installationen
- Bestehende Konfigurationen in der Datenbank bleiben unverändert

## Datei-Kontext
**Datei**: `backend/open_webui/config.py`
**Relevant für**: RAG-Funktionalität, Embedding-Verarbeitung, Text-Chunking