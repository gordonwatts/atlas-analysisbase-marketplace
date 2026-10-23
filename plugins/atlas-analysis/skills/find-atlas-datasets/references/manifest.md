# Analysis dataset manifest

Write YAML with these top-level fields:

- `schema_version`: `1`.
- `inputs`: specification, data-source Markdown and evidence JSON filenames and
  SHA-256 hashes, plus the analysis prompt or its exact stated constraints.
- `complete`: true only when all required sample roles, periods, signal points,
  tiers and field compatibility are resolved; otherwise false.
- `datasets`: one entry per unique, catalog-confirmed analysis-tier DID.
- `gaps`: unresolved requirements/roles, blockers and concrete next actions.

Each dataset entry contains:

- `did`: complete `scope:name`, with no wildcards or placeholders.
- `did_type`: `dataset` or `container`.
- `role`: `data`, `background_mc`, `signal_mc` or `special_stream`.
- `process`, `campaign_or_period`, `energy_tev`, `derivation` and `dsid` (null
  for real data). Preserve unknown metadata as null with an explanation.
- `usage`: nominal, systematic alternative, validation, control or sideband;
  explain overlapping uses without duplicating the DID.
- `requirement_ids`: IDs from the input extraction contract.
- `recommendation`: `status` (official_default, explicit_user_choice,
  provisional_alternative or not_applicable), `source_url`, `section_or_version`,
  `accessed_at`, and `exception_reason` where relevant. Standard Model background
  nominal choices need an applicable central recommendation or an explicit gap.
- `catalog_evidence`: query/service, lookup date, existence result, production
  tags and counts when available; include container membership evidence when
  applicable. A proposed name belongs in `gaps`, not this list.
- `provenance`: MC EVNT DID/AMI identifier and verified parent chain to this
  derivation, PMG paths/include chain and physics confidence; real-data records
  instead identify stream/run and reconstruction provenance.
- `field_compatibility`: `status` (verified, partial or unverified), input probe
  IDs, production scope, uncovered requirement IDs and next checks. Catalog
  existence or a matching tier name alone does not verify field access.
- `coverage`: periods/slices/parameter points covered and any overlap/removal
  rules needed when combining entries.

Keep identities and evidence separate: no speculative DIDs in `datasets`, no
guessed metadata, and no credentials or signed URLs. `datasets: []` is valid for
a blocked search with `complete: false` and explanatory `gaps`. The accompanying
`dataset-selection.md` should explain the scientific choices and summarize the
searches tried, including failed routes, without duplicating full raw responses.
