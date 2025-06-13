# HIVE Auth-Bereich Branding Dokumentation

## 📋 Übersicht
Diese Dokumentation beschreibt alle Änderungen, die zur Anpassung des Auth-Bereichs von "Open WebUI" auf "HIVE" vorgenommen wurden. Alle Dateipfade sind relativ zum Projektroot.

---

## 🎯 Durchgeführte Änderungen

### 1. **APP_NAME Konfiguration**
**Datei:** `src/lib/constants.ts`
**Zeile:** 4
```typescript
export const APP_NAME = 'HIVE';
```
**Ursprünglich:** `'Open WebUI'`
**Zweck:** Zentrale Konfiguration des Anwendungsnamens

---

### 2. **Logo im Auth-Bereich**
**Datei:** `src/routes/auth/+page.svelte`
**Zeilen:** 213-224
```html
<!-- Mittig platziertes Logo -->
<div class="flex justify-center mb-8">
    <img
        id="auth-logo"
        crossorigin="anonymous"
        src="{WEBUI_BASE_URL}/static/splash.png"
        class="w-24 h-24 rounded-full shadow-lg dark:hidden"
        alt="HIVE Logo"
    />
    <img
        id="auth-logo-dark"
        crossorigin="anonymous"
        src="{WEBUI_BASE_URL}/static/splash-dark.png"
        class="w-24 h-24 rounded-full shadow-lg hidden dark:block"
        alt="HIVE Logo"
    />
</div>
```
**Zweck:** Dual-Logo-System für Light/Dark Mode

---

### 3. **Deutsche Übersetzungen**
**Datei:** `src/lib/i18n/locales/de-DE/translation.json`

| Zeile | Schlüssel | Alter Wert | Neuer Wert |
|-------|-----------|------------|------------|
| 654 | `"Get started with {{WEBUI_NAME}}"` | `"Loslegen mit {{WEBUI_NAME}}"` | `"Loslegen mit HIVE"` |
| 1141 | `"Sign in to {{WEBUI_NAME}}"` | `"Bei {{WEBUI_NAME}} anmelden"` | `"Im HIVE anmelden"` |
| 1142 | `"Sign in to {{WEBUI_NAME}} with LDAP"` | `"Bei {{WEBUI_NAME}} mit LDAP anmelden"` | `"Im HIVE mit LDAP anmelden"` |
| 1145 | `"Sign up to {{WEBUI_NAME}}"` | `"Bei {{WEBUI_NAME}} registrieren"` | `"Im HIVE registrieren"` |
| 1147 | `"Signing in to {{WEBUI_NAME}}"` | `"Wird bei {{WEBUI_NAME}} angemeldet"` | `"Anmeldung im HIVE läuft"` |

---

## 🔧 Technische Details

### Logo-Implementation
- **Light Mode Logo:** `static/static/splash.png`
- **Dark Mode Logo:** `static/static/splash-dark.png`
- **CSS-Klassen:** 
  - Light: `dark:hidden`
  - Dark: `hidden dark:block`
- **Größe:** `w-24 h-24` (96x96px)
- **Styling:** `rounded-full shadow-lg`

### Datenfluss der WEBUI_NAME Variable
1. **Quelle:** `src/lib/constants.ts` → `APP_NAME`
2. **Store:** `src/lib/stores/index.ts` → `WEBUI_NAME = writable(APP_NAME)`
3. **Backend Override:** `src/routes/+layout.svelte:581` → `WEBUI_NAME.set(backendConfig.name)`
4. **Verwendung:** `$WEBUI_NAME` in allen Komponenten

---

## 🛠️ Wartung & Anpassungen

### APP_NAME ändern
```typescript
// src/lib/constants.ts
export const APP_NAME = 'NEUER_NAME';
```
**Auswirkung:** Ändert automatisch alle Vorkommen in der gesamten App

### Logo austauschen
1. **Light Mode:** Datei `static/static/splash.png` ersetzen
2. **Dark Mode:** Datei `static/static/splash-dark.png` ersetzen
3. **Format:** PNG empfohlen, quadratisch für beste Darstellung

### Logo-Größe anpassen
**Datei:** `src/routes/auth/+page.svelte`
```html
<!-- Aktuelle Größe: w-24 h-24 (96x96px) -->
class="w-32 h-32 rounded-full shadow-lg"  <!-- Größer: 128x128px -->
class="w-16 h-16 rounded-full shadow-lg"  <!-- Kleiner: 64x64px -->
```

### Übersetzungen hinzufügen/ändern
**Dateipfad:** `src/lib/i18n/locales/[SPRACHE]/translation.json`
- `de-DE/` - Deutsch
- `en-US/` - Englisch
- `fr-FR/` - Französisch
- etc.

### Browser-Titel anpassen
**Statischer Titel:** `src/app.html:104`
```html
<title>OAKMIND HIVE</title>
```

**Dynamischer Titel:** Wird automatisch durch `APP_NAME` gesetzt

---

## 🔍 Debugging & Troubleshooting

### Logo wird nicht angezeigt
1. **Pfad prüfen:** Existiert `static/static/splash.png`?
2. **Berechtigung prüfen:** Sind die Dateien lesbar?
3. **Browser-Cache:** Ctrl+F5 für Hard-Refresh

### Falsche Texte angezeigt
1. **APP_NAME prüfen:** `src/lib/constants.ts:4`
2. **Backend-Config prüfen:** Könnte `backendConfig.name` überschreiben
3. **Spracheinstellung prüfen:** Welche Locale ist aktiv?

### Übersetzungen funktionieren nicht
1. **Datei prüfen:** `src/lib/i18n/locales/de-DE/translation.json`
2. **JSON-Syntax prüfen:** Validator verwenden
3. **Browser neu laden:** i18n wird gecacht

---

## 📁 Betroffene Dateien (Vollständige Liste)

```
src/
├── lib/
│   ├── constants.ts                           # APP_NAME Konfiguration
│   ├── stores/index.ts                        # WEBUI_NAME Store
│   └── i18n/locales/de-DE/translation.json   # Deutsche Übersetzungen
├── routes/
│   ├── auth/+page.svelte                     # Logo + Auth UI
│   └── +layout.svelte                        # Backend Config Override
└── app.html                                   # Statischer Browser-Titel

static/static/
├── splash.png                                 # Light Mode Logo
└── splash-dark.png                           # Dark Mode Logo
```

---

## 🎨 CSS-Klassen Reference

| Klasse | Zweck |
|--------|-------|
| `flex justify-center mb-8` | Logo-Container zentriert mit Abstand |
| `w-24 h-24` | Logo-Größe 96x96px |
| `rounded-full` | Rundes Logo |
| `shadow-lg` | Schatten-Effekt |
| `dark:hidden` | Nur im Light Mode sichtbar |
| `hidden dark:block` | Nur im Dark Mode sichtbar |

---

## 📝 Änderungshistorie

| Datum | Änderung | Dateien |
|-------|----------|---------|
| 10.06.2025 | APP_NAME auf 'HIVE' geändert | `constants.ts` |
| 10.06.2025 | Logo im Auth-Bereich eingefügt | `auth/+page.svelte` |
| 10.06.2025 | Deutsche Übersetzungen angepasst | `de-DE/translation.json` |

---

## 🔄 Rollback-Anleitung

### Zu "Open WebUI" zurückkehren:
1. **APP_NAME zurücksetzen:**
   ```typescript
   // src/lib/constants.ts
   export const APP_NAME = 'Open WebUI';
   ```

2. **Logo entfernen:** Zeilen 213-224 in `src/routes/auth/+page.svelte` löschen

3. **Übersetzungen zurücksetzen:**
   ```json
   "Sign in to {{WEBUI_NAME}}": "Bei {{WEBUI_NAME}} anmelden",
   "Sign in to {{WEBUI_NAME}} with LDAP": "Bei {{WEBUI_NAME}} mit LDAP anmelden",
   ```

---

*📅 Erstellt: 10.06.2025  
🔧 Letztes Update: 10.06.2025  
👤 Bearbeiter: Roo (AI Assistant)*