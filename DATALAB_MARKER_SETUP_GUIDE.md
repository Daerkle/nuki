# Datalab Marker Setup Guide

## Übersicht

Es gibt zwei Möglichkeiten, Marker für die Dokumentenverarbeitung zu verwenden:

1. **Lokale Marker Installation** (`datalab_marker`)
2. **Datalab Marker Cloud API** (`datalab_marker_api`)

## 1. Lokale Marker Installation

### Voraussetzungen
- Docker Container mit Marker Service läuft auf `http://marker:8501`
- Oder lokale Installation auf einem anderen Port

### Konfiguration
1. Gehen Sie zu **Admin Settings > Documents**
2. Wählen Sie bei "Content Extraction Engine": **Datalab Marker (Local)**
3. Geben Sie die Marker Server URL ein: `http://marker:8501` (oder Ihre lokale URL)
4. Konfigurieren Sie optional:
   - Languages: z.B. `en,de,fr`
   - Use LLM: Ein/Aus
   - Skip Cache: Ein/Aus

### Wichtige Hinweise
- Die lokale Marker API unterstützt NICHT alle Parameter der Cloud API
- Folgende Parameter werden NICHT unterstützt:
  - `extract_images`
  - `force_ocr`
  - `paginate`
  - `strip_existing_ocr`
  - `disable_image_extraction`
  - `output_format`

## 2. Datalab Marker Cloud API

### Voraussetzungen
- API-Schlüssel von Datalab

### Konfiguration
1. Gehen Sie zu **Admin Settings > Documents**
2. Wählen Sie bei "Content Extraction Engine": **Datalab Marker Cloud API**
3. Geben Sie Ihren Datalab API-Schlüssel ein

### Unterstützte Parameter
Die Cloud API unterstützt alle verfügbaren Parameter:
- Languages
- Use LLM
- Skip Cache
- Force OCR
- Paginate
- Strip Existing OCR
- Disable Image Extraction
- Output Format

## Fehlerbehebung

### Lokale Marker Fehler
Wenn Sie Fehler wie "500 Internal Server Error" erhalten:
1. Überprüfen Sie, ob der Marker Service läuft
2. Testen Sie die URL direkt: `curl http://marker:8501/health`
3. Schauen Sie in die Logs: `docker logs marker`

### Cloud API Fehler
1. Überprüfen Sie Ihren API-Schlüssel
2. Stellen Sie sicher, dass Sie "Datalab Marker Cloud API" ausgewählt haben
3. Prüfen Sie Ihre Internetverbindung

## Docker Compose Beispiel

```yaml
services:
  marker:
    image: datalab/marker:latest
    ports:
      - "8501:8501"
    environment:
      - MARKER_PORT=8501
    volumes:
      - ./marker_data:/data
```

## Test-Skripte

### Test für lokale Installation
```python
# test_local_marker.py
import requests

url = "http://marker:8501/convert"
files = {'pdf_file': open('test.pdf', 'rb')}
data = {
    'langs': 'en,de',
    'use_llm': 'false',
    'skip_cache': 'false'
}

response = requests.post(url, files=files, data=data)
print(response.status_code)
print(response.json())
```

### Test für Cloud API
```python
# test_cloud_marker.py
import requests

url = "https://api.datalab.to/api/v1/marker"
headers = {"X-Api-Key": "YOUR_API_KEY"}
files = {'pdf_file': open('test.pdf', 'rb')}
data = {
    'langs': 'en,de',
    'force_ocr': 'true',
    'output_format': 'markdown'
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.status_code)
print(response.json())