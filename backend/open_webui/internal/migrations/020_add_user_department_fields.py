"""
Peewee migration: 020_add_user_department_fields
Date: 2024-12-26 21:38:00
"""

import peewee as pw
from open_webui.internal.db import JSONField


def migrate(migrator, database, fake=False, **kwargs):
    """Fügt Department Manager Felder zur User-Tabelle hinzu"""
    
    # Prüfe, ob die Felder bereits existieren
    try:
        # Versuche eine Abfrage mit den neuen Feldern - wenn sie existieren, wird kein Fehler auftreten
        cursor = database.execute_sql("SELECT department, managed_by FROM user LIMIT 1")
        print("Department Manager Felder existieren bereits - Migration übersprungen")
    except Exception:
        # Felder existieren nicht, füge sie hinzu
        print("Füge Department Manager Felder zur User-Tabelle hinzu")
        migrator.add_fields(
            "user",
            department=pw.CharField(null=True, help_text="Abteilungs-Name für Department Manager"),
            managed_by=pw.CharField(null=True, help_text="User-ID des verwaltenden Managers")
        )


def rollback(migrator, database, fake=False, **kwargs):
    """Entfernt Department Manager Felder von der User-Tabelle"""
    
    # Remove fields from User model
    migrator.remove_fields("user", "department", "managed_by")