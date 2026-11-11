<p align="center"><img width="50%" height="100%" alt="logo" src="https://github.com/user-attachments/assets/00ce920d-1daf-4432-8b50-b640c3d8f3c1" /></p>

# Malward VPS — threat database status

This repository publicly displays the current version numbers of Malward VPS security databases.
The table is automatically refreshed hourly by GitHub Actions from the public endpoint
`https://malward-api.jmsoft.pl/public/databases.json`.

A new commit is created only when at least one database version changes.

<!-- VPS_DATABASE_STATUS:START -->
| Database | Version | Change detected (UTC) |
| --- | --- | --- |
| Database bundle | `1.1.0.106.111126` | 2026-11-11 15:29 UTC |
| VPS signatures | `1.2.0.855.111126` | 2026-11-11 15:29 UTC |
| Trusted entries | `1.0.0.859.111126` | 2026-11-11 15:29 UTC |
| Malicious URL database | `1.1.1.248.111126` | 2026-11-11 15:29 UTC |
| Heuristic rules | `1.0.0.477.111126` | 2026-11-11 15:29 UTC |
| Bot IP database | `1.0.0.699.111126` | 2026-11-11 15:29 UTC |
| URL cache | `1.0.0.693.111126` | 2026-11-11 15:29 UTC |
<!-- VPS_DATABASE_STATUS:END -->

## How updates work

The `.github/workflows/update-vps-database-status.yml` workflow runs hourly. The
`.github/scripts/update_vps_versions.py` script retrieves the public database-bundle metadata,
compares it with the table above, and updates only changed versions.

## Download the database bundle

The current bundle version is available as plain text at:

```text
https://malward-api.jmsoft.pl/public/databases.version
```

The complete database bundle is available here:

```text
https://malward-api.jmsoft.pl/public/malward-databases.zip
```

The recommended way to install the bundle is through the Malward application's **Import database
bundle** feature. For an offline or recovery installation, close Malward before copying files and
run the following PowerShell commands. The example installs the **medium** URL-protection profile.

```powershell
$api = 'https://malward-api.jmsoft.pl/public'
$profile = 'medium' # choose: low, medium, or high
$version = (Invoke-RestMethod "$api/databases.version").Trim()
$zip = Join-Path $env:TEMP "malward-databases-$version.zip"
$staging = Join-Path $env:TEMP "malward-databases-$version"
$target = Join-Path $env:ProgramData 'Malward\data'

Invoke-WebRequest "$api/malward-databases.zip" -OutFile $zip
New-Item -ItemType Directory -Force -Path $staging, $target | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath $staging -Force

# Copy the common databases.
Get-ChildItem $staging -Filter '*.vdeb' |
    Where-Object { $_.Name -notlike 'urls-*.vdeb' } |
    Copy-Item -Destination $target -Force

# Install the selected URL-protection profile using the filename expected by Malward.
Copy-Item (Join-Path $staging "urls-$profile.vdeb") (Join-Path $target 'urls.vdeb') -Force

Write-Host "Installed database bundle version $version to $target"
```

The target folder is normally `C:\ProgramData\Malward\data`.
