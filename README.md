# Malward VPS — threat database status

This repository publicly displays the current version numbers of Malward VPS security databases.
The table is automatically refreshed hourly by GitHub Actions from the public endpoint
`https://malward-api.jmsoft.pl/public/databases.json`.

A new commit is created only when at least one database version changes.

<!-- VPS_DATABASE_STATUS:START -->
| Database | Version | Change detected (UTC) |
| --- | --- | --- |
| Database bundle | `—` | — |
| VPS signatures | `—` | — |
| Trusted entries | `—` | — |
| Malicious URL database | `—` | — |
| Heuristic rules | `—` | — |
| Bot IP database | `—` | — |
| URL cache | `—` | — |
<!-- VPS_DATABASE_STATUS:END -->

## How updates work

The `.github/workflows/update-vps-database-status.yml` workflow runs hourly. The
`.github/scripts/update_vps_versions.py` script retrieves the public database-bundle metadata,
compares it with the table above, and updates only changed versions.
