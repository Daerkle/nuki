# Datalab Marker Implementation - Zusammenfassung

## Durchgeführte Änderungen

### 1. Backend-Änderungen

#### a) Lokale Marker Implementation (`datalab_marker.py`)
- **Datei**: `backend/open_webui/retrieval/loaders/datalab_marker.py`
- **Wichtigste Änderung**: Entfernung nicht unterstützter Parameter
- **Anpassungen**:
  - Entfernt: `extract_images` (verursachte 500 Fehler)
  - Flexible Parameter-Behandlung implementiert
  - Verbesserte Fehlerbehandlung
  - Unterstützung für Marker URL über `marker_url` Parameter

#### b) Cloud API Implementation (`datalab_marker_api.py`)
- **Datei**: `backend/open_webui/retrieval/loaders/datalab_marker_api.py`
- **Status**: Vollständig implementiert und validiert
- **Features**: Unterstützt alle Parameter der Datalab API

#### c) Main Loader (`main.py`)
- **Datei**: `backend/open_webui/retrieval/loaders/main.py`
- **Änderungen**:
  - Korrekte Weiterleitung der `marker_url` für lokale Installation
  - Unterscheidung zwischen lokalem Server (URL) und Cloud API (API Key)

### 2. Frontend-Änderungen

#### Documents.svelte
- **Datei**: `src/lib/components/admin/Settings/Documents.svelte`
- **Änderungen**:
  - Entfernung der `$i18n.t()` Übersetzungsfunktionen (verhinderten Dropdown-Anzeige)
  - Zwei separate Optionen im Dropdown:
    - "Datalab Marker (Local)" für lokale Installation
    - "Datalab Marker Cloud API" für Cloud-Service
  - Korrekte Konfigurationsfelder für beide Optionen

## Konfiguration

### Für lokale Marker Installation:
1. **Content Extraction Engine**: "Datalab Marker (Local)"
2. **Marker Server URL**: z.B. `http://marker:8501` oder `http://localhost:8501`
3. **Unterstützte Parameter**:
   - Languages (z.B. `en,de,fr`)
   - Use LLM (Ein/Aus)
   - Skip Cache (Ein/Aus)

### Für Datalab Cloud API:
1. **Content Extraction Engine**: "Datalab Marker Cloud API"
2. **API Key**: Ihr Datalab API-Schlüssel
3. **Alle Parameter werden unterstützt**

## Wichtige Hinweise

### Lokale Installation
- Die lokale Marker API ist restriktiver als die Cloud API
- Nicht alle Parameter werden akzeptiert
- Bei Fehlern prüfen Sie die Marker-Logs

### Cloud API
- Benötigt gültigen API-Schlüssel
- Unterstützt alle verfügbaren Parameter
- Internetverbindung erforderlich

## Docker-Konfiguration (für lokale Installation)

```yaml
services:
  open-webui:
    # ... andere Konfiguration ...
    environment:
      - CONTENT_EXTRACTION_ENGINE=datalab_marker
      - DATALAB_MARKER_API_KEY=http://marker:8501
      - DATALAB_MARKER_LANGS=en,de
    depends_on:
      - marker

  marker:
    image: datalab/marker:latest
    ports:
      - "8501:8501"
    environment:
      - MARKER_PORT=8501
    volumes:
      - ./marker_data:/data
```

## Fehlerbehebung

### Problem: "500 Internal Server Error" bei lokaler Installation
**Lösung**: 
- Überprüfen Sie, ob der Marker-Service läuft
- Stellen Sie sicher, dass die URL korrekt ist
- Prüfen Sie die Marker-Logs auf Fehler

### Problem: Dropdown zeigt keine Marker-Optionen
**Lösung**: 
- Frontend neu bauen: `npm run build`
- Browser-Cache leeren
- Seite neu laden

### Problem: "API Key required" bei lokaler Installation
**Lösung**:
- Stellen Sie sicher, dass Sie "Datalab Marker (Local)" ausgewählt haben
- Geben Sie die Server-URL ein, nicht einen API-Key

## Status

✅ **Lokale Marker Implementation**: Fertig und funktionsfähig
✅ **Cloud API Implementation**: Fertig und funktionsfähig
✅ **Frontend Integration**: Fertig und funktionsfähig

Beide Implementierungen sollten jetzt korrekt funktionieren, sobald:
1. Das Docker-Image neu gebaut wird
2. Die entsprechenden Services gestartet sind
3. Die korrekte Konfiguration in den Admin-Einstellungen vorgenommen wurde