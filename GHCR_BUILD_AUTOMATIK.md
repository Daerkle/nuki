# 🚀 **Automatischer GHCR Build & Deploy für DSGVO-Open WebUI**

## 📋 **Übersicht**

Dieser Build-Prozess ist vollständig automatisiert und optimiert für **Linux/Debian**-Container. Der Workflow wird automatisch ausgelöst bei:
- ✅ Push auf `master` oder `main` Branch
- ✅ Erstellung eines neuen Tags (z.B. `v1.0.0`)
- ✅ Pull Requests (nur Build, kein Push)
- ✅ Manueller Workflow-Start

## 🔧 **Build-Features**

### **Multi-Plattform Support**
- 🐧 **linux/amd64** (Intel/AMD 64-bit)
- 🍓 **linux/arm64** (ARM 64-bit, z.B. Raspberry Pi 4/5)

### **DSGVO-Compliance**
- 🔒 **Keine Admin-Chat-Zugriffe**
- 📊 **Keine Telemetrie/Analytics**
- 🛡️ **Datenschutz-optimiert**

### **Performance-Optimierungen**
- ⚡ **Docker Buildx** für parallele Builds
- 🗄️ **GitHub Actions Cache** für schnellere Builds
- 📦 **Debian Slim Base** für minimale Container-Größe

## 🏷️ **Verfügbare Image-Tags**

### **Automatische Tags:**
```bash
# Neueste Version vom master Branch
ghcr.io/daerkle/oidsgvo:latest

# DSGVO-zertifizierte Version
ghcr.io/daerkle/oidsgvo:dsgvo-compliant

# Branch-spezifische Builds
ghcr.io/daerkle/oidsgvo:master

# Commit-Hash Tags
ghcr.io/daerkle/oidsgvo:master-a1b2c3d
```

### **Release Tags:**
```bash
# Vollständige Versionsnummer
ghcr.io/daerkle/oidsgvo:v1.0.0

# Major.Minor Version
ghcr.io/daerkle/oidsgvo:1.0
```

## 🚀 **Deployment auf Linux/Debian**

### **Docker Compose (Empfohlen)**
```bash
# Repository klonen
git clone https://github.com/Daerkle/oidsgvo.git
cd oidsgvo

# Mit GHCR Image starten
docker-compose -f docker-compose.ghcr.yaml up -d
```

### **Direkter Docker Run**
```bash
docker run -d \
  --name oidsgvo \
  --platform linux/amd64 \
  -p 3000:8080 \
  -e WEBUI_SECRET_KEY= \
  -e ENABLE_ADMIN_EXPORT=false \
  -e ENABLE_ADMIN_CHAT_ACCESS=false \
  -e SCARF_NO_ANALYTICS=true \
  -e DO_NOT_TRACK=true \
  -e ANONYMIZED_TELEMETRY=false \
  -v oidsgvo-data:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/daerkle/oidsgvo:latest
```

### **Für ARM64 (Raspberry Pi)**
```bash
docker run -d \
  --name oidsgvo \
  --platform linux/arm64 \
  -p 3000:8080 \
  -e WEBUI_SECRET_KEY= \
  -e ENABLE_ADMIN_EXPORT=false \
  -e ENABLE_ADMIN_CHAT_ACCESS=false \
  -e SCARF_NO_ANALYTICS=true \
  -e DO_NOT_TRACK=true \
  -e ANONYMIZED_TELEMETRY=false \
  -v oidsgvo-data:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/daerkle/oidsgvo:latest
```

## 🔍 **Build-Status überwachen**

1. **GitHub Actions**: https://github.com/Daerkle/oidsgvo/actions
2. **GHCR Packages**: https://github.com/Daerkle/oidsgvo/pkgs/container/oidsgvo

## 🛠️ **Manueller Build triggern**

```bash
# GitHub CLI verwenden
gh workflow run "Build and Push DSGVO-konforme Open WebUI to GHCR"

# Oder über GitHub Web-Interface:
# Actions → Build and Push DSGVO-konforme Open WebUI to GHCR → Run workflow
```

## 📊 **Build-Metriken**

- ⏱️ **Build-Zeit**: ~8-12 Minuten
- 📦 **Image-Größe**: ~1.2-1.5 GB (komprimiert)
- 🔄 **Cache-Effizienz**: ~60-80% schneller bei wiederholten Builds

## 🔐 **Sicherheits-Features**

- 🛡️ **SBOM-Generierung** (Software Bill of Materials)
- 📋 **Container-Metadaten** für Transparenz
- 🔒 **Non-root Container** Execution
- 🏷️ **Signierte Images** (geplant)

## 🚨 **Troubleshooting**

### **Build schlägt fehl:**
```bash
# Logs überprüfen
gh run list --workflow="Build and Push DSGVO-konforme Open WebUI to GHCR"
gh run view <RUN_ID> --log
```

### **Image nicht verfügbar:**
```bash
# GHCR-Login testen
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Image manuell pullen
docker pull ghcr.io/daerkle/oidsgvo:latest
```

### **Plattform-Probleme:**
```bash
# Verfügbare Plattformen prüfen
docker manifest inspect ghcr.io/daerkle/oidsgvo:latest

# Spezifische Plattform forcieren
docker pull --platform linux/amd64 ghcr.io/daerkle/oidsgvo:latest
```

---
**✅ Ihr DSGVO-konformes Open WebUI läuft automatisch auf jedem Linux/Debian System!**