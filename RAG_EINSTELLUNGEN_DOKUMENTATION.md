# RAG-Einstellungen Dokumentation für Open WebUI

## Übersicht
Diese Dokumentation listet alle verfügbaren RAG (Retrieval-Augmented Generation) Einstellungen in Open WebUI auf, einschließlich der geplanten Änderungen.

## Geplante Änderungen

### 1. DEFAULT_RAG_TEMPLATE Aktualisierung
**Datei**: `backend/open_webui/config.py` (Zeile 2221-2249)
**Änderung**: Ersetzen des aktuellen Templates durch ein neues strukturiertes Format

### 2. Standard-Parameter Aktualisierung
- **RAG_TOP_K**: Von 3 auf 10 erhöhen
- **CHUNK_SIZE**: Von 1000 auf 2000 Tokens erhöhen  
- **CHUNK_OVERLAP**: Von 100 auf 500 Tokens erhöhen

## Vollständige RAG-Konfiguration

### 1. Embedding-Konfiguration
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `RAG_EMBEDDING_ENGINE` | config.py:2115 | "" | Engine für Embeddings ("", "openai", "ollama", "azure_openai") |
| `RAG_EMBEDDING_MODEL` | config.py:2127 | "sentence-transformers/all-MiniLM-L6-v2" | Embedding-Modell |
| `RAG_EMBEDDING_BATCH_SIZE` | config.py:2143 | 1 | Batch-Größe für Embedding-Generierung |
| `RAG_EMBEDDING_QUERY_PREFIX` | config.py:2152 | None | Präfix für Query-Embeddings |
| `RAG_EMBEDDING_CONTENT_PREFIX` | config.py:2154 | None | Präfix für Content-Embeddings |
| `RAG_EMBEDDING_PREFIX_FIELD_NAME` | config.py:2156 | None | Feldname für Embedding-Präfixe |

### 2. Retrieval-Einstellungen
| Parameter | Dateipfad | Standard | Neu | Beschreibung |
|-----------|-----------|----------|-----|--------------|
| `RAG_TOP_K` | config.py:2054 | 3 | **10** | Anzahl der Top-Ergebnisse |
| `RAG_TOP_K_RERANKER` | config.py:2057 | 3 | 3 | Top-K für Reranker |
| `RAG_RELEVANCE_THRESHOLD` | config.py:2062 | 0.0 | 0.0 | Relevanz-Schwellenwert |
| `RAG_HYBRID_BM25_WEIGHT` | config.py:2067 | 0.5 | 0.5 | BM25-Gewichtung für Hybrid-Suche |
| `ENABLE_RAG_HYBRID_SEARCH` | config.py:2073 | false | false | Hybrid-Suche aktivieren |
| `RAG_FULL_CONTEXT` | config.py:2079 | false | false | Vollständigen Kontext verwenden |
| `BYPASS_EMBEDDING_AND_RETRIEVAL` | config.py:2049 | false | false | Embedding und Retrieval umgehen |

### 3. Reranking-Konfiguration
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `RAG_RERANKING_ENGINE` | config.py:2160 | "" | Reranking-Engine |
| `RAG_RERANKING_MODEL` | config.py:2166 | "" | Reranking-Modell |
| `RAG_EXTERNAL_RERANKER_URL` | config.py:2184 | "" | Externe Reranker-URL |
| `RAG_EXTERNAL_RERANKER_API_KEY` | config.py:2190 | "" | API-Schlüssel für externen Reranker |

### 4. Template- und Text-Verarbeitung
| Parameter | Dateipfad | Standard | Neu | Beschreibung |
|-----------|-----------|----------|-----|--------------|
| `DEFAULT_RAG_TEMPLATE` | config.py:2221 | [Aktuelles Template] | **[Neues Template]** | Standard-RAG-Template |
| `RAG_TEMPLATE` | config.py:2251 | DEFAULT_RAG_TEMPLATE | [Neues Template] | Aktuelles RAG-Template |
| `CHUNK_SIZE` | config.py:2212 | 1000 | **2000** | Chunk-Größe in Tokens |
| `CHUNK_OVERLAP` | config.py:2215 | 100 | **500** | Chunk-Überlappung in Tokens |
| `RAG_TEXT_SPLITTER` | config.py:2197 | "" | "" | Text-Splitter-Konfiguration |
| `TIKTOKEN_ENCODING_NAME` | config.py:2205 | "cl100k_base" | "cl100k_base" | Tiktoken-Encoding |

### 5. Datei-Einstellungen
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `RAG_FILE_MAX_COUNT` | config.py:2085 | None | Maximale Anzahl Dateien |
| `RAG_FILE_MAX_SIZE` | config.py:2095 | None | Maximale Dateigröße |
| `RAG_ALLOWED_FILE_EXTENSIONS` | config.py:2105 | [] | Erlaubte Dateierweiterungen |
| `PDF_EXTRACT_IMAGES` | config.py:2121 | false | Bilder aus PDFs extrahieren |

### 6. API-Konfigurationen

#### OpenAI
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `RAG_OPENAI_API_BASE_URL` | config.py:2257 | OPENAI_API_BASE_URL | OpenAI API Base URL |
| `RAG_OPENAI_API_KEY` | config.py:2262 | OPENAI_API_KEY | OpenAI API Schlüssel |

#### Azure OpenAI  
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `RAG_AZURE_OPENAI_BASE_URL` | config.py:2268 | "" | Azure OpenAI Base URL |
| `RAG_AZURE_OPENAI_API_KEY` | config.py:2273 | "" | Azure OpenAI API Schlüssel |
| `RAG_AZURE_OPENAI_API_VERSION` | config.py:2278 | "" | Azure OpenAI API Version |

#### Ollama
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `RAG_OLLAMA_BASE_URL` | config.py:2284 | OLLAMA_BASE_URL | Ollama Base URL |
| `RAG_OLLAMA_API_KEY` | config.py:2290 | "" | Ollama API Schlüssel |

### 7. Weitere Einstellungen
| Parameter | Dateipfad | Standard | Beschreibung |
|-----------|-----------|----------|--------------|
| `ENABLE_RAG_LOCAL_WEB_FETCH` | config.py:2297 | false | Lokales Web-Fetching aktivieren |
| `ENABLE_WEB_LOADER_SSL_VERIFICATION` | main.py:711 | - | SSL-Verifikation für Web-Loader |

## Neues DEFAULT_RAG_TEMPLATE

```
Generate Response to User Query  
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
<context>{{CONTEXT}}</context>
```

## Implementierungsschritte

1. **Template aktualisieren**: DEFAULT_RAG_TEMPLATE in config.py ersetzen
2. **Parameter anpassen**: 
   - RAG_TOP_K: 3 → 10
   - CHUNK_SIZE: 1000 → 2000  
   - CHUNK_OVERLAP: 100 → 500
3. **Tests durchführen**: Sicherstellen, dass alle RAG-Funktionen weiterhin funktionieren
4. **Dokumentation aktualisieren**: Diese Dokumentation bei Bedarf erweitern

## Dateien zur Bearbeitung

- `backend/open_webui/config.py` - Hauptkonfigurationsdatei
- `backend/open_webui/main.py` - Anwendung der Konfigurationen
- `backend/open_webui/routers/retrieval.py` - RAG-Router und Endpunkte

## Wichtige Hinweise

- Alle Parameter mit `PersistentConfig` werden in der Datenbank gespeichert
- Änderungen an Standard-Werten betreffen nur neue Installationen
- Bestehende Konfigurationen bleiben unverändert, es sei denn, sie werden explizit zurückgesetzt
- Die Vector-Datenbank-Konfiguration befindet sich in `backend/open_webui/retrieval/vector/`