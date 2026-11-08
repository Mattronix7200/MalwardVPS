# Malward VPS — status baz zagrożeń

Ten projekt publicznie pokazuje aktualne numery wersji baz ochronnych Malward VPS.
Tabela jest automatycznie odświeżana co godzinę przez GitHub Actions na podstawie publicznego
endpointu `https://malward-api.jmsoft.pl/public/databases.json`.

Nowy commit jest tworzony tylko wtedy, gdy co najmniej jedna wersja bazy się zmieni.

<!-- VPS_DATABASE_STATUS:START -->
| Baza | Wersja | Zmiana wykryta (UTC) |
| --- | --- | --- |
| Pakiet baz | `—` | — |
| Sygnatury VPS | `—` | — |
| Lista zaufanych wpisów | `—` | — |
| Baza złośliwych URL | `—` | — |
| Reguły heurystyczne | `—` | — |
| Baza Bot IP | `—` | — |
| Pamięć podręczna URL | `—` | — |
<!-- VPS_DATABASE_STATUS:END -->

## Jak działa aktualizacja

Workflow `.github/workflows/update-vps-database-status.yml` uruchamia się co godzinę. Skrypt
`.github/scripts/update_vps_versions.py` pobiera metadane publicznego pakietu baz, porównuje je z
tabelą powyżej i aktualizuje wyłącznie zmienione wersje.
