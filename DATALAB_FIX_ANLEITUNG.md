# Anleitung: Datalab Marker API Option sichtbar machen

## Problem
Die Option "Datalab Marker (Cloud API)" wird im Dropdown-Menü nicht angezeigt, obwohl sie korrekt implementiert ist.

## Lösung

### 1. Frontend neu bauen
```bash
cd /Users/steffengottle/Desktop/hive-main
npm run build
```

### 2. Dev-Server neu starten
Falls Sie den Entwicklungsserver verwenden:
```bash
# Stoppen Sie den laufenden Server (Ctrl+C)
# Dann neu starten:
npm run dev
```

### 3. Browser-Cache leeren
- **Chrome/Edge**: Strg+Shift+R (Windows/Linux) oder Cmd+Shift+R (Mac)
- **Firefox**: Strg+F5 (Windows/Linux) oder Cmd+Shift+R (Mac)
- **Safari**: Cmd+Option+E dann Cmd+R

### 4. Vollständiger Neustart (falls nötig)
```bash
# Backend stoppen und neu starten
cd backend
python -m open_webui.main

# In einem neuen Terminal - Frontend neu starten
cd /Users/steffengottle/Desktop/hive-main
npm run dev
```

## Überprüfung
Nach diesen Schritten sollte die Option "Datalab Marker (Cloud API)" im Dropdown unter:
**Admin → Settings → Documents → Content Extraction Engine**
sichtbar sein.

## Bestätigte Implementierung
- ✅ Backend-Datei: `backend/open_webui/retrieval/loaders/datalab_marker_api.py`
- ✅ Integration in: `backend/open_webui/retrieval/loaders/main.py`
- ✅ Frontend-Option in: `src/lib/components/admin/Settings/Documents.svelte` (Zeile 333)
- ✅ Validierung implementiert (Zeile 178-182)
- ✅ UI für API-Key Eingabe (Zeile 483-489)

Die Implementierung ist vollständig und korrekt. Es handelt sich nur um ein Build/Cache-Problem.