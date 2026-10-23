#!/usr/bin/env python3
"""Check the returned evidence contract; no services or third-party packages."""
import argparse
import hashlib
import json
from pathlib import Path

STATUSES = {"verified", "derived", "external", "backup", "unavailable", "unverified"}


class EvidenceError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise EvidenceError(message)


def index_records(records, name):
    need(isinstance(records, list), f"{name} must be a list")
    result = {}
    for row in records:
        need(isinstance(row, dict), f"Each {name} entry must be an object")
        identity = row.get("id")
        need(isinstance(identity, str) and identity.strip(), f"{name} needs nonempty IDs")
        need(identity not in result, f"Duplicate {name} ID: {identity}")
        result[identity] = row
    return result


def references(row, key):
    values = row.get(key, [])
    need(isinstance(values, list) and all(isinstance(x, str) for x in values),
         f"{row['id']}: {key} must be a list of IDs")
    return values


def validate(workspace):
    workspace = Path(workspace).resolve()
    ledger_path = workspace / "data-source-evidence.json"
    if not ledger_path.is_file():
        hint = " Found it under probes/; the deliverable belongs in the workspace root." if (
            workspace / "probes/data-source-evidence.json"
        ).is_file() else ""
        raise EvidenceError(f"Missing root deliverable: {ledger_path}.{hint}")
    table = workspace / "data-sources.md"
    need(table.is_file() and bool(table.read_text(encoding="utf-8").strip()),
         "Missing or empty root deliverable: data-sources.md")
    try:
        data = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as error:
        raise EvidenceError(f"Invalid evidence JSON: {error}") from error
    need(isinstance(data, dict) and data.get("schema_version") == 1,
         "Expected evidence object with schema_version 1")
    spec = data.get("specification")
    need(isinstance(spec, dict) and isinstance(spec.get("path"), str),
         "Missing specification path/hash")
    source = Path(spec["path"])
    if not source.is_absolute():
        source = workspace / source
    need(source.is_file(), f"Specification file not found: {source}")
    need(spec.get("sha256") == hashlib.sha256(source.read_bytes()).hexdigest(),
         "Specification SHA-256 does not match the input file")
    need(isinstance(data.get("models"), dict), "Missing models object")
    need(isinstance(data.get("unresolved"), list), "Missing unresolved list")
    requirements = index_records(data.get("requirements"), "requirement")
    need(bool(requirements), "The requirement inventory is empty")
    probes = index_records(data.get("probes"), "probe")
    for identity, probe in probes.items():
        need(probe.get("status") in {"succeeded", "failed", "blocked"},
             f"{identity}: invalid probe status")
        if probe.get("status") == "succeeded" and probe.get("transport") != "external":
            need(bool(probe.get("query")), f"{identity}: missing returned executed query")
            observations = probe.get("observations")
            need(isinstance(observations, dict) and type(observations.get("entries")) is int
                 and observations["entries"] >= 0 and isinstance(observations.get("columns"), dict)
                 and bool(observations["columns"]),
                 f"{identity}: missing observed entry count/columns")
    for identity, row in requirements.items():
        need(row.get("status") in STATUSES, f"{identity}: invalid requirement status")
        deps = references(row, "depends_on")
        evidence = references(row, "probe_ids")
        need(set(deps) <= requirements.keys(), f"{identity}: unknown dependency ID")
        need(set(evidence) <= probes.keys(), f"{identity}: unknown probe ID")
        if row["status"] == "backup":
            need(row.get("backup_for") in requirements, f"{identity}: unknown backup_for ID")
        if row["status"] == "verified":
            successful = [probes[x] for x in evidence if probes[x]["status"] == "succeeded"
                          and probes[x].get("transport") != "external"]
            need(any(p.get("observations", {}).get("entries", 0) > 0 for p in successful),
                 f"{identity}: verified claim lacks nonempty ServiceX evidence")
        if row["status"] == "derived":
            need(bool(deps) and all(requirements[x]["status"] in {"verified", "derived", "external"}
                                   for x in deps), f"{identity}: derived inputs are not verified")
    return {"requirements": len(requirements), "probes": len(probes),
            "workspace": str(workspace), "structural_validation": "passed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.workspace)))
    except (EvidenceError, OSError) as error:
        parser.exit(1, f"Evidence validation failed: {error}\n")


if __name__ == "__main__":
    main()
