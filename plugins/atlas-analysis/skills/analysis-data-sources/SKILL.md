---
name: analysis-data-sources
description: Map an ATLAS analysis specification to extraction-ready data sources and verify fields with ServiceX. Use to produce data-sources.md, choose PHYSLITE versus richer derivations, identify missing inputs, and document tested backups. Dataset discovery alone belongs to find-atlas-datasets.
---

# Analysis data sources

Read the supplied analysis specification (`specification.md` by default) and write
`data-sources.md`: a complete extraction contract for the next coding agent.
A source is authoritative only within the sample, production, backend release,
and quantity actually tested. Preserve unresolved physics choices.

Use the installed `iris-hep:servicex` skill for query construction, accessor
discovery and delivery, and UChicago AF tools/skills for catalog and metadata
inspection where available. If dependencies or credentials are unavailable,
finish the inventory and mark affected sources **unverified**, with the exact
blocker. Do not substitute direct input ROOT reads for ServiceX extraction tests.
Reading ServiceX-returned ROOT files with uproot is appropriate. Never put
credentials or signed URLs in deliverables.

## Inventory and sample scope

- Assign stable requirement IDs and cite specification sections. Cover selections,
  all ABCD/control/validation regions and sidebands, trigger decisions/matching,
  noncollision estimates, detector quality, truth/lifetime studies, weights,
  normalization and systematic variations. A nominal skim must not remove fail
  regions or timing sidebands.
- Distinguish event, object, file, sample and run/luminosity-block scope. Include
  identity/join keys, object ordering/associations, type/cardinality, units, and
  whether each value is extracted, derived or external. Include the raw inputs
  to derived quantities.
- Use provided samples first; discover missing candidates with AF tools or
  `find-atlas-datasets`. Track data, background MC, signal MC and special-stream
  roles separately. A multijet MC smoke sample cannot verify LLP truth, data
  trigger menus, or empty/unpaired-stream availability.
- Keep the requested run/energy/object definitions. For an explicit Run 1 to Run 3
  migration, distinguish source requirements from proposed replacements. Do not
  assume modern trigger names, luminosities, calibrations, cross sections,
  good-track definitions or generated lifetimes.

Check that the Python dependencies and user-supplied ServiceX client configuration
are available before probing. Catalog MCP authentication does not configure the
Python delivery client. A missing import is a dependency repair: prepare a local
environment with uv when installation is within the task, rather than treating
it as a ServiceX outage. Inspect configuration presence without printing tokens;
do not include configuration files in returned artifacts.

## PHYSLITE first, with executable probes

1. Start with compatible **DAOD_PHYSLITE** samples for relevant sample classes.
   Record exact DIDs/file provenance, campaign/production tags, query/backend
   releases and calibration state. Inspect release-matched stubs/headers and
   slimming content for unusual accessors. A header proves an API, not retention.
2. Build small ServiceX probes with positive controls (event identity and ordinary
   kinematics), initially **NFiles=1**. Group safe related fields; isolate uncertain
   decorations/links/tools. Include event keys and preserve object alignment.
   Fetch sideband inputs before analysis cuts. Save runnable code and dependency
   versions. Use an event limit only if supported by the actual backend.
3. Execute delivery and materialize lazy output paths. Inspect the returned tree:
   nonzero events, relevant nonempty collections, columns/types, finite/range
   checks, units and association integrity. Save counts and representative
   summaries. Empty arrays, sentinels, defaults or all-false decisions do not
   establish the intended measurement. Record native units, returned units and
   the exact conversion. Transport success and physics equivalence are separate.
4. Classify failure as query/type/translation, authentication/transport/service,
   missing stored content, or insufficient sample coverage. Use accessor
   discovery to repair query errors. A failed query or zero selected events alone
   is **not proof of absence**. Preserve diagnostics and a successful positive
   control. Limit each failing probe to two informed repairs; then isolate it and
   continue independent probes.
5. Try **DAOD_PHYS only for demonstrated PHYSLITE content gaps**, retaining the
   PHYSLITE evidence. If access is blocked, any richer-format investigation is
   provisional. If PHYS demonstrably lacks the requirement, investigate a
   specialist derivation using actual production/content evidence. A derivation
   name does not prove content. Verify richer-format fields through ServiceX too.

Use the ServiceX skill's local diagnostic procedure for failed hosted queries
when appropriate, retaining both results. Local executor success must say which
executor was tested; it does not erase a hosted failure. If worker logs cannot be
retrieved, preserve the request ID/blocker and continue independent probes.

## Backups, metadata and combinations

- For each missing nominal field, evaluate a PHYSLITE-only **backup**: exact
  accessor/inputs, evidence, changed definition, expected physics loss and
  closure/efficiency tests needed. A different track cone/threshold/vertex/quality
  summary is not the specified good-track multiplicity. Prompt jets do not
  silently replace displaced calorimeter jets. If no defensible backup exists,
  say so; never promote it silently to nominal.
- A mixed PHYSLITE/PHYS extraction needs compatible parent provenance, stream/event
  coverage, stable event keys and object matching, including ambiguities and
  unmatched objects. DSID plus row position is not an event join. Different
  objects/calibrations require an explicit mapping. Until checked, label the
  augmentation **proposed, join unverified**.
- Normalization, cut-bookkeeper sums of weights (including negative weights),
  cross sections/filter efficiencies/k-factors, GRLs, trigger prescales/live time,
  generated lifetimes and branching fractions often live outside event trees.
  Give the exact file/catalog/service, key, units, version and retrieval tool.
  Never infer a full-sample denominator from one-file/selected ServiceX output.
  Test file metadata with ServiceX if supported; otherwise verify its external
  route separately and label it **external, not ServiceX-verified**. Inaccessible
  external inputs remain unverified.
- A kinematic accessor does not verify CP calibration, trigger efficiency or a
  systematic. Identify producing tools/configurations and inputs/conditions.
  A shifted nominal number is not a verified systematic.

## Model roles

Keep interpretation, equivalence/backup decisions and final review with the
steering model. When model-selectable delegation is available and authorized,
assign bounded ServiceX lookup/coding/repair to a **luna** worker (for example
`gpt-6-luna`, subject to installed availability). Use the
[probe brief](references/probe-brief.md). Review code and observed outputs before
accepting conclusions. If delegation/model selection is unavailable, work
directly and disclose that fact; never claim a cheaper worker was used merely
because it was recommended.

## Deliver and audit

Read [the evidence contract](references/evidence-contract.md). Deliver:

- `data-sources.md`, with tables grouped by scope/sample role and one row per
  requirement, plus clearly marked backup rows. Columns: item/proposed column;
  short purpose/threshold; scope/type/cardinality; extraction tool and exact code
  reference/accessor (or formula/dependencies); native-to-returned units (blank
  if dimensionless); derivation/source; status/evidence IDs. Escape Markdown pipes
  in formulas (for example absolute eta). Keep types separate from units and
  name the actual external retrieval tool for metadata. Link long probe
  details instead of repeating DIDs in every row.
- `data-source-evidence.json`, the requirements/probe ledger, and `probes/`
  containing executable code, dependency versions, output inspections and
  failure logs, with relative links.
- A conclusion stating nominal coverage, PHYSLITE-only coverage and physics cost,
  richer-format needs, unsupported sample roles, unresolved specification choices,
  unverified joins and actual model roles/repairs/blockers.

Reconcile every inventory requirement with a table row and ledger entry. Audit
verified claims against observed columns, derived claims against verified
dependencies, backups against semantic differences, and absence claims against
scoped content evidence. Do not announce complete readiness with required gaps.
