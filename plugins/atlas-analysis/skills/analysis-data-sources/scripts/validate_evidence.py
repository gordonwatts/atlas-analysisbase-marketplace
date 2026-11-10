#!/usr/bin/env python3
"""Check evidence structure and optional analysis-specific coverage; no services."""
import hashlib
import json
from pathlib import Path
import typer

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


def validate_coverage(data, probes, acceptance, require_complete):
    expected = index_records(acceptance.get("coverage"), "acceptance coverage")
    actual = index_records(data.get("coverage"), "coverage")
    missing = []
    for identity, contract in expected.items():
        need(identity in actual, f"Missing coverage block: {identity}")
        block = actual[identity]
        role = contract.get("sample_role")
        need(isinstance(role, str) and role and block.get("sample_role") == role,
             f"{identity}: sample_role differs from acceptance")
        names = contract.get("checks")
        need(isinstance(names, list) and names and all(isinstance(x, str) for x in names),
             f"{identity}: acceptance checks must be nonempty names")
        checks = block.get("checks")
        need(isinstance(checks, dict), f"{identity}: missing checks object")
        for name in names:
            check = checks.get(name)
            label = f"{identity}/{name}"
            need(isinstance(check, dict), f"Missing coverage check: {label}")
            need(check.get("status") in {"verified", "unverified", "unavailable"},
                 f"{label}: invalid coverage status")
            need(isinstance(check.get("summary"), str) and check["summary"].strip(),
                 f"{label}: summary/blocker required")
            refs = check.get("probe_ids", [])
            need(isinstance(refs, list) and all(isinstance(x, str) and x in probes for x in refs),
                 f"{label}: invalid probe references")
            if check["status"] != "verified":
                missing.append(label)
                continue
            evidence = [probes[x] for x in refs if probes[x].get("status") == "succeeded"
                        and probes[x].get("transport") == "servicex"
                        and probes[x].get("sample_role") == role
                        and probes[x].get("observations", {}).get("entries", 0) > 0]
            need(evidence, f"{label}: lacks nonempty ServiceX evidence for {role}")
            columns = check.get("columns")
            need(isinstance(columns, list) and columns and all(isinstance(x, str) for x in columns),
                 f"{label}: observed columns required")
            observed = set().union(*(p["observations"]["columns"].keys() for p in evidence))
            need(set(columns) <= observed, f"{label}: column absent from scoped observations")
    need(not require_complete or not missing, "Incomplete coverage: " + ", ".join(missing))
    return {"coverage_complete": not missing, "missing_coverage": missing}


def validate(workspace, acceptance=None, require_complete=False):
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
    result = {"requirements": len(requirements), "probes": len(probes),
              "workspace": str(workspace), "structural_validation": "passed"}
    need(not require_complete or acceptance is not None,
         "--require-complete needs an analysis-specific --acceptance contract")
    if acceptance is not None:
        contract = json.loads(Path(acceptance).read_text(encoding="utf-8"))
        need(isinstance(contract, dict) and contract.get("schema_version") == 1,
             "Expected acceptance object with schema_version 1")
        result.update(validate_coverage(data, probes, contract, require_complete))
    return result


def main(workspace: Path = typer.Option(...), acceptance: Path | None = None,
         require_complete: bool = False):
    try:
        print(json.dumps(validate(workspace, acceptance, require_complete)))
    except (EvidenceError, OSError, ValueError) as error:
        typer.echo(f"Evidence validation failed: {error}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(main)
