# Malward VPS — threat database status

This repository publicly displays the current version numbers of Malward VPS security databases.
The table is automatically refreshed hourly by GitHub Actions from the public endpoint
`https://malward-api.jmsoft.pl/public/databases.json`.

A new commit is created only when at least one database version changes.

<!-- VPS_DATABASE_STATUS:START -->
| Database | Version | Change detected (UTC) |
| --- | --- | --- |
| Database bundle | `1.1.0.40.110826` | 2026-11-08T15:21:18Z |
| VPS signatures | `1.2.0.793.110826` | 2026-11-08T15:21:18Z |
| Trusted entries | `1.0.0.796.110826` | 2026-11-08T15:21:18Z |
| Malicious URL database | `1.1.1.185.110826` | 2026-11-08T15:21:18Z |
| Heuristic rules | `1.0.0.414.110826` | 2026-11-08T15:21:18Z |
| Bot IP database | `1.0.0.636.110826` | 2026-11-08T15:21:18Z |
| URL cache | `1.0.0.630.110826` | 2026-11-08T15:21:18Z |
<!-- VPS_DATABASE_STATUS:END -->

## How updates work

The `.github/workflows/update-vps-database-status.yml` workflow runs hourly. The
`.github/scripts/update_vps_versions.py` script retrieves the public database-bundle metadata,
compares it with the table above, and updates only changed versions.
