# Analysis dataset table

Write `datasets.md` unless the user specifies another output name. Identify the
input specification, data-source Markdown and evidence ledger, their hashes,
and any additional analysis constraints before the table.

Use one row per resolved Rucio DID, with these columns:

| Column | Content |
| --- | --- |
| Sample/process and role | Data, background MC, signal MC or special stream; nominal, systematic, validation, control or sideband use |
| Rucio DID | Complete catalog-confirmed `scope:name`, including all production tags |
| DID type | Dataset or container; verify container members' tier and coverage |
| Period/campaign | Requested data period or MC campaign and collision energy |
| Data tier | Actual derivation required by the input access contract |
| Requirements covered | Input requirement IDs, including special-stream/control-region needs |
| Recommendation/evidence | Applicable central nominal recommendation and catalog query/source references |
| Status/gaps | Dataset existence and field compatibility stated separately, with unresolved checks |

Keep an unresolved row for each required sample, period, slice or signal point
without a confirmed DID. Write **unresolved** in that row's DID column and give
the blocker and next action; do not insert speculative names or wildcard queries.
Do not collapse a required sample family into a single representative smoke
sample. Shared DIDs can cover multiple requirements without duplicate rows.

Below the table, provide:

- Central recommendation URLs, sections/list versions and access dates. Explain
  deviations, inaccessible recommendations, nominal versus systematic choices,
  and provisional alternatives. PMG job options alone do not prove nominal status.
- Catalog query/service, lookup date, existence and membership evidence, and
  available production metadata. Preserve unknown values as unknown.
- MC EVNT ancestry/AMI chain and PMG paths with physics confidence. For real
  data, give stream/run and reconstruction provenance instead.
- Field-compatibility evidence scoped to input probe IDs and tested production;
  catalog existence or the same tier name alone does not verify field access.
- Coverage and overlap handling for periods, slices, campaigns and container
  members, plus a reconciliation of every input role/requirement to rows or gaps.
- A clear complete/incomplete conclusion and remaining actions. A blocked search
  still returns a table and an incomplete conclusion, never invented DIDs.

Use short evidence IDs in table cells and resolve them below the table to keep
it readable. Keep identifiers intact in code spans and escape Markdown pipes.
Do not include credentials or signed URLs. Produce a machine-readable companion
only when requested; the Markdown table is the primary deliverable.
