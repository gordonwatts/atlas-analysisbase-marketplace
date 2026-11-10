# Compact evidence contract

The returned deliverables are `data-sources.md` and `data-source-evidence.json`,
both in the analysis workspace root. Working files under `probes/` stay local
unless the user requests debugging artifacts. A requested ROOT smoke file is a
separate deliverable. Never include credentials or signed download URLs.

The Markdown is the full extraction contract. The JSON is a compact index of
requirements and self-contained observations, not an archive of every attempt.
Use stable IDs in both. Keep shared datasets, versions and queries once; omit
repeated prose, raw catalog listings, whole package/source snapshots and full logs.
An unavailable local script is not a usable evidence reference for the reader.

## Ledger shape

Use schema version 1. The example below is an unverified requirement, not a
measurement; replace its source path and hash with the actual input values.

```json
{
  "schema_version": 1,
  "specification": {"path": "specification.md", "sha256": "actual SHA-256"},
  "models": {"steering": "actual model or unavailable", "workers": []},
  "requirements": [
    {
      "id": "jet-pt",
      "spec_ref": "Object definitions / baseline jet",
      "column": "jet_pt",
      "status": "unverified",
      "probe_ids": [],
      "depends_on": [],
      "limitation": "Not probed yet; test the relevant production and object definition."
    }
  ],
  "probes": [],
  "unresolved": []
}
```

Keep each requirement once, including unverified inputs. The Markdown supplies
its purpose, scope, type, units, derivation and source proposal; those fields may
also be included in JSON when useful, without duplicating paragraphs. Backups
have separate IDs and `backup_for` referencing a nominal ID. All dependency and
probe references must resolve. Use scope event, object, file, sample,
luminosity-block or derived; dimensionless units are empty strings.

| Status | Evidence required |
| --- | --- |
| `verified` | Successful ServiceX extraction, nonempty observed values, resolved semantics/units and the applicable sample role |
| `derived` | Formula and dependency IDs, with required inputs verified for compatible events/objects/roles; record whether evaluated |
| `external` | Executed non-event metadata inspection, exact source/tool/key/version; not ServiceX-verified |
| `backup` | `backup_for`, changed semantics and physics cost, extraction status and remaining validation |
| `unavailable` | Scoped retained-content evidence with a successful positive control; not just an API/network error |
| `unverified` | Proposed source or blocker and a concrete next action |

## Role-to-source plan

Include a compact role-to-source table in the Markdown. Optionally add
`sample_roles` to the version-1 JSON ledger, with records containing `id`,
`spec_ref`, `requiredness` (required/conditional/alternative),
`activation_condition`, `source_kind` (event_source/selection/external),
`parent_role_id` (null if unknown), `requirement_ids`, `period_scope`, and
`relationship_evidence` (including checks still needed). All role/requirement
references must resolve. These describe planning intent, not successful probes.
Existing version-1 ledgers without this optional collection remain valid;
downstream discovery derives the plan from their Markdown and specification.

## Probe records

Every probe has unique `id`, `status` (`succeeded`, `failed` or `blocked`) and
`transport` (normally `servicex` or `external`). Include:

- Exact dataset/file, derivation, sample role and production; backend release and
  safe endpoint, or explicit unknowns. Shared sample records may be referenced.
- `query`: the exact executed query for a ServiceX success, plus essential imports
  or helper definitions. Include the final successful form rather than all
  superseded scripts. Record code/query hashes with unambiguous labels when used.
- Dependency versions, command or executor, timestamp and cache status when known;
  factor common runtime information into a shared record. Package version alone
  does not establish the hosted backend release.
- ServiceX request ID, or null and the reason it was unavailable.
- For a successful ServiceX probe, `observations`: an object with `entries`,
  `tree`, and `columns` recording observed types, non-null/nonempty counts,
  native/returned units, conversion and finite/range checks. Include association
  and alignment checks when they matter. Empty/sentinel arrays cannot verify a
  requirement even if transport succeeded.
- For failures, a short sanitized error category/message, affected requirements,
  positive-control ID, informed repairs and next action. Preserve full diagnostics
  locally; include only decisive excerpts. A failed mixed query verifies no
  uninspected field and does not establish missing stored content.

External successes record their retrieval tool/arguments and observed metadata;
they cannot verify event accessors. Joins need input provenance, identity keys,
uniqueness/overlap counts, object matching and ambiguities.

Keep evidence needed to distinguish extraction from physics equivalence: a stored
EM fraction may not establish a calibrated hadronic/EM ratio; a kinematic query
does not validate a displaced-jet calibration. Full normalization cannot be
inferred from a selected one-file output. For track-count backups, the official
[PHYSLITE inventory](https://atlas-physlite-content-opendata.web.cern.ch/opendata_pp_physlite_variables.html)
describes `NumTrkPt1000` as a vertex-indexed ghost-associated loose-track count,
not an exact hit-qualified cone count. Check the target production and vector type.

## Delivery check

Create/checkpoint the root ledger while working, even when probes are blocked.
Before reporting completion run `scripts/validate_evidence.py --workspace` using
this skill's absolute script path and the absolute analysis workspace. It checks
file location, JSON parsing, input hash and structural claim/reference consistency.
Then reconcile the Markdown inventory/status counts and review scientific claims.
Do not move the final ledger into `probes/` or substitute a link to it there.
