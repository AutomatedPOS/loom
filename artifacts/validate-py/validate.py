#!/usr/bin/env python3
"""Validate a loom-warp tree of thread.json files. Exit 1 on ERROR."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "thread.schema.json"

GUID_POINTERS = (
    "supersedes",
    "abandonedScope",
    "realizedAs",
    "voidedPlan",
    "mitigatedBy",
    "blockedBy",
)

SKIP_DIR_NAMES = {".git", "__pycache__", ".venv", "node_modules", "_incoming"}

GUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
CROSS_POINTER_RE = re.compile(
    r"^([A-Za-z0-9][A-Za-z0-9._\-]*):"
    r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$"
)


def load_schema() -> Draft202012Validator:
    with SCHEMA_PATH.open(encoding="utf-8") as fh:
        schema = json.load(fh)
    return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)


def iter_thread_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo.rglob("thread.json"):
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(repo).parts):
            continue
        files.append(path)
    return sorted(files)


def walk_nodes(data: dict, location: str, file_path: Path | None, container_guid: str | None):
    yield location, data, file_path, container_guid
    guid = data.get("guid") if isinstance(data.get("guid"), str) else None
    for i, child in enumerate(data.get("threads") or []):
        if isinstance(child, dict):
            yield from walk_nodes(child, f"{location}#/threads/{i}", None, guid)


def is_empty_parent(value) -> bool:
    return value is None or value == ""


def folder_children(repo: Path, file_path: Path) -> list[Path]:
    parent = file_path.parent
    found = []
    for child_dir in sorted(p for p in parent.iterdir() if p.is_dir()):
        candidate = child_dir / "thread.json"
        if candidate.is_file():
            found.append(candidate)
    return found


def nearest_ancestor_thread(repo: Path, file_path: Path) -> Path | None:
    """Nearest ancestor directory that holds thread.json. None if none."""
    current = file_path.parent.parent
    root = repo.resolve()
    while True:
        candidate = current / "thread.json"
        if candidate.is_file():
            return candidate
        if current.resolve() == root:
            return None
        nxt = current.parent
        if nxt == current:
            return None
        current = nxt


def guid_from_thread_file(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    guid = data.get("guid")
    return guid if isinstance(guid, str) else None


def parse_guid_pointer(value: str) -> tuple[str | None, str | None]:
    """Return (repo_or_None, guid) or (None, None) if the form is wrong."""
    if GUID_RE.match(value):
        return None, value
    matched = CROSS_POINTER_RE.match(value)
    if matched:
        return matched.group(1), matched.group(2)
    return None, None


def validate_repo(repo: Path) -> int:
    validator = load_schema()
    errors: list[str] = []
    warnings: list[str] = []

    files = iter_thread_files(repo)
    if not files:
        errors.append(f"ERROR {repo}: no thread.json found")
        print("\n".join(errors), file=sys.stderr)
        return 1

    nodes: list[tuple[str, dict, Path | None, str | None]] = []
    guid_index: dict[str, list[str]] = {}

    for file_path in files:
        loc = str(file_path.relative_to(repo)).replace("\\", "/")
        try:
            with file_path.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            errors.append(f"ERROR {loc}: not JSON ({exc})")
            continue
        if not isinstance(data, dict):
            errors.append(f"ERROR {loc}: document must be one node object")
            continue

        schema_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        for err in schema_errors:
            path = "/".join(str(p) for p in err.absolute_path)
            where = f"{loc}:{path}" if path else loc
            errors.append(f"ERROR {where}: schema {err.message}")

        for node_loc, node, node_file, container_guid in walk_nodes(
            data, loc, file_path, None
        ):
            nodes.append((node_loc, node, node_file, container_guid))
            guid = node.get("guid")
            if isinstance(guid, str) and guid:
                guid_index.setdefault(guid, []).append(node_loc)

    for guid, locs in guid_index.items():
        if len(locs) > 1:
            joined = ", ".join(locs)
            errors.append(f"ERROR duplicate guid {guid}: {joined}")

    root_file = repo / "thread.json"

    for node_loc, node, file_path, container_guid in nodes:
        parent = node.get("isPartOf")
        is_repo_root_file = file_path is not None and file_path.resolve() == root_file.resolve()
        if is_empty_parent(parent):
            if not is_repo_root_file:
                errors.append(
                    f"ERROR {node_loc}: isPartOf empty anywhere but the repo root"
                )
        elif isinstance(parent, str):
            if parent not in guid_index:
                errors.append(
                    f"ERROR {node_loc}: isPartOf {parent} names a node not in this repo"
                )
            else:
                expected: str | None = None
                if file_path is not None and not is_repo_root_file:
                    ancestor = nearest_ancestor_thread(repo, file_path)
                    if ancestor is not None:
                        expected = guid_from_thread_file(ancestor)
                elif container_guid:
                    expected = container_guid
                if expected is not None and parent != expected:
                    errors.append(
                        f"ERROR {node_loc}: isPartOf does not match folder position "
                        f"(expected {expected})"
                    )

        for field in GUID_POINTERS:
            value = node.get(field)
            if not isinstance(value, str) or not value:
                continue
            repo_name, guid = parse_guid_pointer(value)
            if guid is None:
                continue
            if repo_name is not None:
                warnings.append(
                    f"WARNING {node_loc}: {field} points outside this repo ({value})"
                )
                continue
            if guid not in guid_index:
                warnings.append(
                    f"WARNING {node_loc}: {field} {value} names a node not in this repo"
                )

        if node.get("type") == "decision":
            chosen = []
            if file_path is not None:
                for child_file in folder_children(repo, file_path):
                    try:
                        child = json.loads(child_file.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        continue
                    if child.get("type") == "option" and child.get("state") == "chosen":
                        rel = str(child_file.relative_to(repo)).replace("\\", "/")
                        chosen.append(rel)
            for i, child in enumerate(node.get("threads") or []):
                if isinstance(child, dict) and child.get("type") == "option" and child.get("state") == "chosen":
                    chosen.append(f"{node_loc}#/threads/{i}")
            if len(chosen) != 1:
                errors.append(
                    f"ERROR {node_loc}: decision must have exactly one chosen option beneath it (found {len(chosen)})"
                )

        if file_path is not None:
            represented = node.get("representedBy")
            if isinstance(represented, str) and represented.strip():
                target = (file_path.parent / represented).resolve()
                if not target.exists():
                    warnings.append(
                        f"WARNING {node_loc}: representedBy path does not resolve ({represented})"
                    )

            supersedes = node.get("supersedes")
            reason = node.get("supersededBecause")
            if isinstance(supersedes, str) and supersedes:
                if not isinstance(reason, str) or not reason.strip():
                    warnings.append(
                        f"WARNING {node_loc}: supersededBecause thin or empty"
                    )

    for line in errors:
        print(line, file=sys.stderr)
    for line in warnings:
        print(line, file=sys.stderr)

    if errors:
        print(f"{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"ok - {len(nodes)} node(s), {len(warnings)} warning(s)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate loom-warp thread.json trees.")
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Repo root. The thread.json in this directory may have empty isPartOf.",
    )
    args = parser.parse_args(argv)
    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"ERROR {repo}: not a directory", file=sys.stderr)
        return 1
    return validate_repo(repo)


if __name__ == "__main__":
    sys.exit(main())
