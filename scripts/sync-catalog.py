#!/usr/bin/env python3
"""Camp mother: pull hub.json + APP_VER from each registered app repo into apps/catalog.json."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "apps" / "registry.json"
CATALOG_PATH = ROOT / "apps" / "catalog.json"
HUB_PATH = "hub.json"
VERSION_RE = re.compile(
    r"""(?:APP_VER(?:SION)?|const VERSION)\s*[=:]\s*['"]([^'"]+)['"]"""
)

OWNER_DEFAULT = "azzabazza11"


def token() -> str:
    return (
        os.environ.get("HUB_SYNC_TOKEN")
        or os.environ.get("GH_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
        or ""
    ).strip()


def api_get(url: str) -> tuple[int, bytes, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "aaron-apps-hub-camp-mother",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    t = token()
    if t:
        headers["Authorization"] = f"Bearer {t}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return res.status, res.read(), res.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b"", ""


def get_file(owner: str, repo: str, path: str, branch: str) -> tuple[int, str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    status, body, _ = api_get(url)
    if status != 200:
        return status, ""
    data = json.loads(body.decode("utf-8"))
    if data.get("encoding") == "base64" and data.get("content"):
        import base64

        raw = base64.b64decode(data["content"])
        return 200, raw.decode("utf-8", errors="replace")
    download = data.get("download_url")
    if not download:
        return 422, ""
    status2, body2, _ = api_get(download)
    return status2, body2.decode("utf-8", errors="replace") if status2 == 200 else ""


def first_version(text: str) -> str | None:
    m = VERSION_RE.search(text or "")
    return m.group(1) if m else None


def load_local_hub(local_root: Path) -> dict | None:
    p = local_root / HUB_PATH
    if not p.exists():
        return None
    return json.loads(p.read_text())


def merge_app(entry: dict, hub: dict | None, code_version: str | None, issues: list[str]) -> dict:
    card = {
        "id": entry["id"],
        "repo": entry.get("repo"),
        "branch": entry.get("branch", "main"),
        "title": entry["id"],
        "category": "Apps",
        "desc": "",
        "accent": "#44ffaa",
        "icon": "◇",
        "platforms": ["desktop"],
        "status": "soon",
        "installable": False,
        "desktopUrl": "",
        "appUrl": "",
        "version": "",
        "tags": [],
        "changelog": [],
        "issues": issues,
    }
    if hub:
        for key in (
            "title",
            "category",
            "desc",
            "accent",
            "icon",
            "platforms",
            "status",
            "installable",
            "desktopUrl",
            "appUrl",
            "version",
            "tags",
            "changelog",
        ):
            if key in hub and hub[key] not in (None, ""):
                card[key] = hub[key]
    if code_version:
        card["codeVersion"] = code_version
        if card["version"] and card["version"] != code_version:
            issues.append(f"hub.json version {card['version']} != APP_VER {code_version}")
        if not card["version"]:
            card["version"] = code_version
    card["issues"] = issues
    return card


def sync() -> dict:
    registry = json.loads(REGISTRY_PATH.read_text())
    owner = registry.get("owner", OWNER_DEFAULT)
    local_map = {}
    extra = os.environ.get("HUB_LOCAL_MAP", "")
    if extra:
        for pair in extra.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                local_map[k.strip()] = Path(v.strip())

    apps = []
    ok = 0
    for entry in registry["apps"]:
        issues = []
        hub = None
        code_version = None
        repo = entry["repo"]
        branch = entry.get("branch", "main")
        local = local_map.get(entry["id"])

        if local:
            hub = load_local_hub(local)
            if hub is None:
                issues.append("missing hub.json")
            for rel in entry.get("versionFiles") or []:
                p = local / rel
                if p.exists():
                    code_version = first_version(p.read_text(errors="replace"))
                    if code_version:
                        break
        else:
            status, text = get_file(owner, repo, HUB_PATH, branch)
            if status == 200:
                try:
                    hub = json.loads(text)
                except json.JSONDecodeError:
                    issues.append("hub.json is not valid JSON")
            elif status == 404:
                issues.append("missing hub.json")
            else:
                issues.append(f"could not read hub.json (HTTP {status})")
            for rel in entry.get("versionFiles") or []:
                st, src = get_file(owner, repo, rel, branch)
                if st == 200:
                    code_version = first_version(src)
                    if code_version:
                        break

        if hub is None:
            issues.append("using registry stub until hub.json exists")
        else:
            ok += 1
        apps.append(merge_app(entry, hub, code_version, issues))

    catalog = {
        "hub": "Aaron's Apps",
        "syncedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "camp-mother",
        "ok": ok,
        "total": len(apps),
        "apps": apps,
    }
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n")
    return catalog


if __name__ == "__main__":
    cat = sync()
    print(f"synced {cat['ok']}/{cat['total']} apps -> {CATALOG_PATH}")
    drifts = [a for a in cat["apps"] if a.get("issues")]
    for a in drifts:
        print(f"  ! {a['id']}: {'; '.join(a['issues'])}")

