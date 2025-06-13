# 📦 **DSGVO-Open WebUI auf GitHub Container Registry (GHCR) veröffentlichen**

## 🚀 **Schritt 1: GitHub Personal Access Token erstellen**

1. Gehen Sie zu: https://github.com/settings/tokens
2. Klicken Sie "Generate new token" → "Generate new token (classic)"
3. **Scopes auswählen:**
   - ✅ `write:packages` 
   - ✅ `read:packages`
   - ✅ `delete:packages` (optional)
4. Token kopieren und sicher speichern

## 🔧 **Schritt 2: Docker für GHCR konfigurieren**

```bash
# Mit GitHub anmelden (Username und Token eingeben)
echo "IHR_GITHUB_TOKEN" | docker login ghcr.io -u IHR_GITHUB_USERNAME --password-stdin

# Beispiel:
echo "ghp_xxxxxxxxxxxx" | docker login ghcr.io -u Daerkle --password-stdin
```

## 🏗️ **Schritt 3: Image builden und taggen**

```bash
# In das Repository-Verzeichnis wechseln
cd oidsgvo

# Image für GHCR builden
docker build -t ghcr.io/daerkle/oidsgvo:latest .
docker build -t ghcr.io/daerkle/oidsgvo:v1.0.0 .

# Zusätzlich mit DSGVO-Tag
docker build -t ghcr.io/daerkle/oidsgvo:dsgvo-compliant .
```

## 📤 **Schritt 4: Auf GHCR pushen**

```bash
# Images auf GHCR hochladen
docker push ghcr.io/daerkle/oidsgvo:latest
docker push ghcr.io/daerkle/oidsgvo:v1.0.0
docker push ghcr.io/daerkle/oidsgvo:dsgvo-compliant
```

## 📋 **Schritt 5: Docker-Compose für GHCR aktualisieren**

Erstellen Sie eine neue `docker-compose.ghcr.yaml`:

```yaml
services:
  open-webui:
    image: ghcr.io/daerkle/oidsgvo:latest
    container_name: open-webui-dsgvo
    volumes:
      - open-webui:/app/backend/data
    ports:
      - "3000:8080"
    environment:
      - 'WEBUI_SECRET_KEY='
      - 'ENABLE_ADMIN_EXPORT=false'
      - 'ENABLE_ADMIN_CHAT_ACCESS=false'
      - 'SCARF_NO_ANALYTICS=true'
      - 'DO_NOT_TRACK=true'
      - 'ANONYMIZED_TELEMETRY=false'
    extra_hosts:
      - host.docker.internal:host-gateway
    restart: unless-stopped

volumes:
  open-webui: {}
```

## 🌐 **Schritt 6: Für alle nutzbar machen**

Jetzt können andere das DSGVO-konforme Image direkt verwenden:

```bash
# Direkt von GHCR starten
docker run -d \
  --name oidsgvo \
  -p 3000:8080 \
  -e WEBUI_SECRET_KEY= \
  -e ENABLE_ADMIN_EXPORT=false \
  -e ENABLE_ADMIN_CHAT_ACCESS=false \
  -e SCARF_NO_ANALYTICS=true \
  -e DO_NOT_TRACK=true \
  -e ANONYMIZED_TELEMETRY=false \
  -v oidsgvo-data:/app/backend/data \
  ghcr.io/daerkle/oidsgvo:latest

# Oder mit Docker Compose
curl -O https://raw.githubusercontent.com/Daerkle/oidsgvo/master/docker-compose.ghcr.yaml
docker-compose -f docker-compose.ghcr.yaml up -d
```

## 🔄 **Schritt 7: Automatisches Building (GitHub Actions)**

Erstellen Sie `.github/workflows/build-ghcr.yml`:

```yaml
name: Build and Push to GHCR

on:
  push:
    branches: [ master ]
    tags: [ 'v*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: daerkle/oidsgvo

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=raw,value=latest,enable={{is_default_branch}}
          type=raw,value=dsgvo-compliant

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
```

## 📖 **Schritt 8: README für GHCR aktualisieren**

```markdown
# 🔒 DSGVO-konforme Open WebUI

## Schnellstart mit GHCR:

```bash
docker run -d \
  --name oidsgvo \
  -p 3000:8080 \
  -e WEBUI_SECRET_KEY= \
  -e ENABLE_ADMIN_EXPORT=false \
  -e ENABLE_ADMIN_CHAT_ACCESS=false \
  -e SCARF_NO_ANALYTICS=true \
  -e DO_NOT_TRACK=true \
  -e ANONYMIZED_TELEMETRY=false \
  ghcr.io/daerkle/oidsgvo:latest
```

## Verfügbare Tags:
- `latest` - Neueste Version
- `v1.0.0` - Stable Release
- `dsgvo-compliant` - DSGVO-zertifiziert
```

## 🎯 **Vorteile von GHCR:**

✅ **Öffentlich verfügbar** - Jeder kann das Image verwenden
✅ **Versionierung** - Verschiedene Tags für Releases  
✅ **Automatisches Building** - CI/CD mit GitHub Actions
✅ **Kostenlos** - Für öffentliche Repositories
✅ **Integriert** - Direkt mit GitHub verbunden

---
**Ihr DSGVO-konformes Open WebUI ist jetzt weltweit verfügbar!** 🌍🔒