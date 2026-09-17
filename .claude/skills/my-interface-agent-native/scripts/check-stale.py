#!/usr/bin/env python3
"""Source-fingerprint tooling for the my-interface-agent-native adapter.

Three commands:

  check   (default) Read .claude/interface-sync.yaml, re-hash every recorded
          source, and report which native artifacts are provably stale.
          Exit 1 when any entry is stale or missing, else 0.

  stamp   Used by Agent Sync for Constructed Skills. Re-hash each Interface-owned
          Skill Contract, write the fingerprint into the native SKILL.md
          frontmatter `metadata` block, and update the synchronization record.

  record  Used by Agent Sync for every other declaration (Rule, Hook, Permission,
          Agent Instance, Extension, Integration, setting, empty category, ...).
          Hash the sources Agent Sync names and update the synchronization
          record. Their native artifacts offer no free-form metadata field, so
          the fingerprint lives in the record only.

A changed fingerprint proves staleness. An unchanged fingerprint never proves
conformance; only a full section-by-section comparison does. This script
therefore never emits a status on its own: the status it records is the one
Agent Sync passes in.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import re
import sys
from pathlib import Path

import yaml

RECORD = Path(".claude/interface-sync.yaml")
SKILL_PROFILE = Path(".interface/agent/skill/profile.yaml")
SKILLS_DIR = Path(".claude/skills")
SKILL_MECHANISM = "Claude Code project Skill"


def project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".claude").is_dir() and (parent / ".interface").is_dir():
            return parent
    sys.exit("check-stale.py: project root (with .claude/ and .interface/) not found")


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------- frontmatter
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def read_frontmatter(text: str) -> tuple[str, dict]:
    m = FM_RE.match(text)
    if not m:
        return "", {}
    return m.group(1), (yaml.safe_load(m.group(1)) or {})


def _q(v: object) -> str:
    return yaml.safe_dump(v, default_style='"').strip()


def write_metadata(path: Path, meta: dict) -> None:
    """Replace or insert the `metadata:` block without touching other fields."""
    text = path.read_text()
    m = FM_RE.match(text)
    if not m:
        sys.exit(f"{path}: no frontmatter")
    fm = m.group(1)
    block = "metadata:\n" + "".join(f"  {k}: {_q(v)}\n" for k, v in meta.items())
    lines = fm.split("\n")
    out, i, replaced = [], 0, False
    while i < len(lines):
        if lines[i].startswith("metadata:"):
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i] == ""):
                i += 1
            out.append(block.rstrip("\n"))
            replaced = True
            continue
        out.append(lines[i])
        i += 1
    if not replaced:
        out.append(block.rstrip("\n"))
    path.write_text("---\n" + "\n".join(out) + "\n---\n" + text[m.end():])


# ---------------------------------------------------------------- declarations
def constructed_skills(root: Path) -> list[dict]:
    """Every Skill the Human-owned Skill Profile declares with a Contract and no prepared file.

    Groups are discovered from the Profile on every call, never from a fixed list.
    """
    prof = yaml.safe_load((root / SKILL_PROFILE).read_text())
    settings = prof["content"]["settings"]
    files_dir = root / (settings.get("skill_files") or {}).get("directory", "")
    found = []
    for group in (settings.get("project_skills") or {}).values():
        if not isinstance(group, dict):
            continue
        for key, decl in group.items():
            if not isinstance(decl, dict) or "contract" not in decl or "name" not in decl:
                continue
            if (files_dir / f"{key}.md").is_file() or (files_dir / key).is_dir():
                print(f"skip {decl['name']}: Prepared (owned by Skill Installer)")
                continue
            found.append({"key": key, "name": decl["name"], "contract": decl["contract"]})
    return found


# ---------------------------------------------------------------- record
def entry_sources(entry: dict) -> list[dict]:
    """Sources of a record entry, reading the older single-source shape too."""
    if "sources" in entry:
        return entry["sources"]
    if "source" in entry:
        return [{"path": entry["source"], "fingerprint": entry.get("fingerprint")}]
    return []


def write_record(root: Path, entries: list[dict], mode: str, ts: str, result: str) -> None:
    rec_path = root / RECORD
    previous = (yaml.safe_load(rec_path.read_text()) if rec_path.exists() else {}) or {}
    replaced = {e["declaration"] for e in entries}
    kept = [e for e in previous.get("declarations", []) if e["declaration"] not in replaced]
    last_run = {"mode": mode, "at": ts, "result": result or (previous.get("last_run") or {}).get("result", "")}
    record = {
        "meta": {
            "path": str(RECORD),
            "purpose": "Machine-readable synchronization record written by my-interface-agent-native. Fingerprints prove staleness, never conformance.",
            "owner": "my-interface-agent-native",
        },
        "last_run": last_run,
        "declarations": sorted(kept + entries, key=lambda e: e["declaration"]),
    }
    rec_path.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=120))
    print(f"wrote {RECORD} ({len(entries)} updated, {len(kept)} kept)")


# ---------------------------------------------------------------- commands
def cmd_check(root: Path) -> int:
    rec_path = root / RECORD
    if not rec_path.exists():
        print(f"no synchronization record at {RECORD}; run Agent Sync first")
        return 1
    rec = yaml.safe_load(rec_path.read_text()) or {}
    rows, bad = [], 0
    for d in rec.get("declarations", []):
        sources = entry_sources(d)
        artifact = d.get("artifact") or ""
        missing = [s["path"] for s in sources if not (root / s["path"]).exists()]
        changed = [s["path"] for s in sources if s["path"] not in missing and sha256(root / s["path"]) != s.get("fingerprint")]
        if missing:
            state, bad = f"missing source: {', '.join(missing)}", bad + 1
        elif artifact and not (root / artifact).exists():
            state, bad = "missing artifact", bad + 1
        elif changed:
            state, bad = f"STALE (source changed since last sync: {', '.join(changed)})", bad + 1
        elif d.get("realized_as") == SKILL_MECHANISM:
            _, fm = read_frontmatter((root / artifact).read_text())
            stamped = (fm.get("metadata") or {}).get("contract_sha256")
            if stamped != sources[0].get("fingerprint"):
                state, bad = "STALE (artifact stamp differs from record)", bad + 1
            else:
                state = "fingerprint unchanged (not proof of conformance)"
        else:
            state = "fingerprint unchanged (not proof of conformance)"
        rows.append((artifact or d["declaration"], d.get("status", "?"), state))
    width = max(len(r[0]) for r in rows) if rows else 10
    print(f"last run: {rec.get('last_run', {})}")
    for a, s, st in rows:
        print(f"{a.ljust(width)}  [{s}]  {st}")
    print(f"\n{bad} stale/missing of {len(rows)}")
    return 1 if bad else 0


def cmd_stamp(root: Path, mode: str, status: str, note: str, result: str, only: list[str]) -> int:
    ts = now()
    entries = []
    for d in constructed_skills(root):
        if only and d["name"] not in only:
            continue
        src = root / d["contract"]
        art = root / SKILLS_DIR / d["name"] / "SKILL.md"
        if not src.exists() or not art.exists():
            print(f"skip {d['name']}: missing {'contract' if not src.exists() else 'SKILL.md'}")
            continue
        fp = sha256(src)
        write_metadata(art, {"contract": d["contract"], "contract_sha256": fp, "synced_at": ts})
        entries.append({
            "declaration": f"agent/skill/contracts/{Path(d['contract']).name}",
            "sources": [{"path": d["contract"], "fingerprint": fp}],
            "realized_as": SKILL_MECHANISM,
            "artifact": str(SKILLS_DIR / d["name"] / "SKILL.md"),
            "status": status,
            "mode": mode,
            "at": ts,
            **({"note": note} if note else {}),
        })
        print(f"stamped {art.relative_to(root)}")
    write_record(root, entries, mode, ts, result)
    return 0


def cmd_record(root: Path, args: argparse.Namespace) -> int:
    ts = now()
    sources = []
    for s in args.source:
        if not (root / s).is_file():
            sys.exit(f"record: source not found: {s}")
        sources.append({"path": s, "fingerprint": sha256(root / s)})
    entry = {
        "declaration": args.declaration,
        "sources": sources,
        "realized_as": args.realized_as,
        **({"artifact": args.artifact} if args.artifact else {}),
        **({"provider": args.provider} if args.provider else {}),
        "status": args.status,
        "mode": args.mode,
        "at": ts,
        **({"note": args.note} if args.note else {}),
    }
    write_record(root, [entry], args.mode, ts, args.result)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("check")
    st = sub.add_parser("stamp")
    rc = sub.add_parser("record")
    for p in (st, rc):
        p.add_argument("--mode", required=True, choices=["self", "module"])
        p.add_argument("--status", required=True)
        p.add_argument("--note", default="")
        p.add_argument("--result", default="")
    st.add_argument("--only", nargs="*", default=[], help="native skill names to stamp; default every Constructed Skill")
    rc.add_argument("--declaration", required=True, help="Module declaration, e.g. agent/rule/profile.yaml#project_rules.interface-bootstrap")
    rc.add_argument("--source", nargs="+", required=True, help="every Module source read for this declaration")
    rc.add_argument("--realized-as", required=True, help="Claude Code mechanism, or 'none' for an empty or blocked declaration")
    rc.add_argument("--artifact", default="", help="project path of the native artifact, when one exists")
    rc.add_argument("--provider", default="", help="provider identity when the realization is not a project file")
    args = ap.parse_args()
    root = project_root()
    if args.cmd == "stamp":
        return cmd_stamp(root, args.mode, args.status, args.note, args.result, args.only)
    if args.cmd == "record":
        return cmd_record(root, args)
    return cmd_check(root)


if __name__ == "__main__":
    sys.exit(main())
