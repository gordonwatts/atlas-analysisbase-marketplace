# Evidence contract

The Markdown table is the human interface. The JSON ledger makes claims
auditable; neither alone proves a query ran. Preserve executed code, observed
outputs and logs with relative paths. Keep compact inspections when large ROOT
files cannot be returned. Exclude credentials and signed URLs.

Use this structure (example values below are not measured results):

```json
{
  "schema_version": 1,
  "specification": {"path": "specification.md", "sha256": "..."},
  "models": {"steering": "actual model or unavailable", "workers": []},
  "requirements": [
    {
      "id": "jet-pt",
      "spec_ref": "Object definitions / baseline jet",
      "item": "jet transverse momentum",
      "column": "jet_pt",
      "purpose": "baseline threshold as specified",
      "scope": "object",
      "type": "var * float32",
      "native_units": "MeV",
      "returned_units": "GeV",
      "source": "ServiceX: jet.pt()/1000.0; probes/jets.py:query",
      "derivation": "DAOD_PHYSLITE",
      "sample_roles": ["background-mc"],
      "status": "unverified",
      "probe_ids": [],
      "depends_on": [],
      "limitation": "example only; extraction has not run"
    }
  ],
  "probes": [],
  "unresolved": []
}
```

`scope`: event, object, file, sample, luminosity-block, or derived.
Dimensionless units are `""`. Each requirement ID appears once. Backups have
their own IDs and `backup_for` referencing the nominal ID. Different sample
coverage can use separate IDs.

| Status | Required evidence |
| --- | --- |
| `verified` | Successful ServiceX extraction, observed column/values, resolved semantics/units and applicable sample role, all scoped in a probe |
| `derived` | Formula and dependency IDs; necessary raw inputs verified for compatible events/objects/sample roles; say whether the formula itself was tested |
| `external` | Exact non-event source, tool/key/version and successful executed inspection; explicitly not ServiceX-verified |
| `backup` | `backup_for`, changed semantics/physics cost, dependency/probe evidence and further validation needed; say whether extraction succeeded |
| `unavailable` | Scoped content evidence or controlled missing-content failure with successful positive control; not a network/API-only error |
| `unverified` | Proposed source or blocker with reason and next action |

Each `probes` entry records:

- `id`, exact `dataset`/input-file provenance, `derivation`, `sample_role`,
  production tags and backend release (or explicit unknowns).
- `code` path and SHA-256 of executed code, dependency versions, command,
  timestamp, backend endpoint without secrets, ServiceX request ID when available
  and cache status. If the client does not expose it, use `request_id: null`
  with a reason; never invent an ID.
- `status`: `succeeded`, `failed`, or `blocked`. Separate service completion
  from output-inspection success. Record attempted requirements and sample
  applicability. A mixed failure verifies no uninspected field.
- Success: output paths, tree, entry count, per-column observed type,
  nonempty/non-null counts and representative range/value checks; supported
  requirement IDs and inspection artifact. Empty truth/object arrays cannot
  verify their accessor values. Retain unit evidence.
- Failure/blocker: error category, exact diagnostic/log path, affected requirement
  IDs, positive-control probe ID, informed repairs and next action. Distinguish
  API support, retained content, sample coverage and access. Scope absence
  conclusions to the tested production.

External metadata probes use `transport: "external"`; they cannot establish
ServiceX-verified event accessors. Join checks need input provenance, identity
keys, uniqueness/overlap counts, object-matching rule and ambiguities.

Finish with counts by status, reconciled with the Markdown table. Backup rows do
not count as nominal coverage. A minimal successful probe does not validate the
whole ledger.

For track-count backups, check stored shape before choosing a template type.
The [official OpenData PHYSLITE inventory](https://atlas-physlite-content-opendata.web.cern.ch/opendata_pp_physlite_variables.html)
documents `AnalysisJets.NumTrkPt1000` as one vector of counts per jet, indexed
by vertex, using ghost association and a loose track selection. It is not a
scalar or the CalRatio hit-qualified cone count. Check the target production
and installed package's vector template support; this inventory alone does
not establish retention in another production or successful ServiceX access.