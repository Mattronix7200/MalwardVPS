#!/usr/bin/env python3
"""Update the VPS database-version table in README.md from the public API."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://malward-api.jmsoft.pl/public/databases.json"
README_PATH = Path("README.md")
START_MARKER = "<!-- VPS_DATABASE_STATUS:START -->"
END_MARKER = "<!-- VPS_DATABASE_STATUS:END -->"

DATABASES = (
    ("Database bundle", "bundle"),
    ("VPS signatures", "vps"),
    ("Trusted entries", "whitelist"),
    ("Malicious URL database", "urls"),
    ("Heuristic rules", "heur"),
    ("Bot IP database", "botip"),
    ("URL cache", "urlcache"),
)


def get_payload() -> dict:
    request = Request(
        API_URL,
        headers={"Accept": "application/json", "User-Agent": "Malward-VPS-README-Bot/1.0"},
    )
    try:
        with urlopen(request, timeout=30) as response:  # nosec B310 - fixed HTTPS endpoint
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not retrieve VPS database metadata: {error}") from error

    if not isinstance(payload, dict) or payload.get("ready") is not True:
        raise RuntimeError("The VPS database bundle is not ready; README was not changed.")
    return payload


def existing_timestamps(table: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for label, version, changed_at in re.findall(r"^\| (.+?) \| `([^`]+)` \| (.+?) \|$", table, re.MULTILINE):
        rows[label] = (version, changed_at)
    return rows


def render_table(payload: dict, old_rows: dict[str, tuple[str, str]]) -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    versions = dict(payload.get("databases") or {})
    versions["bundle"] = {"version": payload.get("version", "—")}

    lines = [
        START_MARKER,
        "| Database | Version | Change detected (UTC) |",
        "| --- | --- | --- |",
    ]
    for label, key in DATABASES:
        value = versions.get(key, {})
        version = str(value.get("version") or "—")
        previous = old_rows.get(label)
        changed_at = previous[1] if previous and previous[0] == version else now
        lines.append(f"| {label} | `{version}` | {changed_at} |")
    lines.append(END_MARKER)
    return "\n".join(lines)


def main() -> int:
    if not README_PATH.is_file():
        raise RuntimeError("README.md was not found.")

    readme = README_PATH.read_text(encoding="utf-8")
    marker_pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL,
    )
    match = marker_pattern.search(readme)
    if not match:
        raise RuntimeError("The VPS database table markers are missing from README.md.")

    payload = get_payload()
    replacement = render_table(payload, existing_timestamps(match.group(0)))
    updated = readme[: match.start()] + replacement + readme[match.end() :]

    if updated == readme:
        print("No VPS database version changes detected.")
        return 0

    README_PATH.write_text(updated, encoding="utf-8")
    print("Updated the VPS database-version table in README.md.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"::error::{error}", file=sys.stderr)
        raise SystemExit(1)
