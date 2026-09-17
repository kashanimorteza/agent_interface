#!/usr/bin/env python3
"""Source-fingerprint tooling for the my-interface-agent-sync adapter.

Two commands:

  check   (default) Read .claude/interface-sync.yaml, re-hash every recorded
          source, and report which native artifacts are provably stale.
          Exit 1 when any entry is stale or missing, else 0.

  stamp   Used by Agent Sync after reconciliation. Re-hash every Interface-owned
          Skill Contract, write the fingerprint into each native SKILL.md
          frontmatter `metadata` block, and rewrite the synchronization record.

A changed fingerprint proves staleness. An unchanged fingerprint never proves
conformance; only a full section-by-section comparison does. This script
therefore never emits "synchronized" on its own: the status it records is the
one Agent Sync passes in.
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
MECHANISM = "Claude Code project Skill"


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
def declared_skills(root: Path) -> list[dict]:
    """name -> contract mapping from the Human-owned Skill Profile (read only by Agent Sync)."""
    prof = yaml.safe_load((root / SKILL_PROFILE).read_text())
    groups = prof["content"]["settings"]["project_skills"]
    found = []
    for group in ("core_workflow", "supporting"):
        for key, decl in (groups.get(group) or {}).items():
            if "contract" in decl and "name" in decl:
                found.append({"key": key, "name": decl["name"], "contract": decl["contract"]})
    return found


# ---------------------------------------------------------------- commands
def cmd_check(root: Path) -> int:
    rec_path = root / RECORD
    if not rec_path.exists():
        print(f"no synchronization record at {RECORD}; run Agent Sync first")
        return 1
    rec = yaml.safe_load(rec_path.read_text()) or {}
    rows, bad = [], 0
    for d in rec.get("declarations", []):
        src = root / d["source"]
        art = root / d["artifact"]
        if not src.exists():
            state, bad = "missing source", bad + 1
        elif not art.exists():
            state, bad = "missing artifact", bad + 1
        elif sha256(src) != d.get("fingerprint"):
            state, bad = "STALE (source changed since last sync)", bad + 1
        else:
            _, fm = read_frontmatter(art.read_text())
            stamped = (fm.get("metadata") or {}).get("contract_sha256")
            if stamped != d.get("fingerprint"):
                state, bad = "STALE (artifact stamp differs from record)", bad + 1
            else:
                state = "fingerprint unchanged (not proof of conformance)"
        rows.append((d["artifact"], d.get("status", "?"), state))
    width = max(len(r[0]) for r in rows) if rows else 10
    print(f"last run: {rec.get('last_run', {})}")
    for a, s, st in rows:
        print(f"{a.ljust(width)}  [{s}]  {st}")
    print(f"\n{bad} stale/missing of {len(rows)}")
    return 1 if bad else 0


def cmd_stamp(root: Path, mode: str, status: str, note: str, result: str, only: list[str]) -> int:
    ts = now()
    entries = []
    for d in declared_skills(root):
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
            "source": d["contract"],
            "fingerprint": fp,
            "realized_as": MECHANISM,
            "artifact": str(SKILLS_DIR / d["name"] / "SKILL.md"),
            "status": status,
            "mode": mode,
            "at": ts,
            **({"note": note} if note else {}),
        })
        print(f"stamped {art.relative_to(root)}")
    rec_path = root / RECORD
    previous = yaml.safe_load(rec_path.read_text()) if rec_path.exists() else {}
    kept = [e for e in (previous or {}).get("declarations", []) if e["artifact"] not in {n["artifact"] for n in entries}]
    record = {
        "meta": {
            "path": str(RECORD),
            "purpose": "Machine-readable synchronization record written by my-interface-agent-sync. Fingerprints prove staleness, never conformance.",
            "owner": "my-interface-agent-sync",
        },
        "last_run": {"mode": mode, "at": ts, "result": result},
        "declarations": sorted(kept + entries, key=lambda e: e["artifact"]),
    }
    rec_path.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=120))
    print(f"wrote {RECORD} ({len(entries)} updated, {len(kept)} kept)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("check")
    st = sub.add_parser("stamp")
    st.add_argument("--mode", required=True, choices=["self", "module"])
    st.add_argument("--status", default="activation required")
    st.add_argument("--note", default="")
    st.add_argument("--result", default="")
    st.add_argument("--only", nargs="*", default=[], help="native skill names to stamp; default all declared")
    args = ap.parse_args()
    root = project_root()
    if args.cmd == "stamp":
        return cmd_stamp(root, args.mode, args.status, args.note, args.result, args.only)
    return cmd_check(root)


if __name__ == "__main__":
    sys.exit(main())
