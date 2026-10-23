# Analysis dataset table

Write `datasets.md` unless the user specifies another output name. Identify the
input specification, data-source Markdown and evidence ledger, their hashes,
and any additional analysis constraints before the table.

## Scope before expansion

Start with a short role-to-source table: role ID, specification reference,
required/conditional/alternative, activation condition, physical source versus
selection/external dependency, parent source if known, and period scope.
Conditional roles are not required until their criterion is met. Keep inactive
families in a decision table; do not expand all their DSIDs/campaigns. If useful
candidates were already found, put them in a separate optional table. Use official
central defaults when an SM role is activated.

Record selected years and their matching MC campaigns. If unspecified, state a
bounded discovery scenario and its assumptions without approving that range.
Retain all necessary slices/points within that scenario and state how to extend
it; do not silently select one year just to shorten the manifest. Unknown year
scope is one decision, not a missing dataset for every possible year.

Several regions can share one source. Map ABCD/control selections to that source
once, conditional on trigger, bunch-group, skim and field retention. Statistical
independence does not itself require a separate DID. Empty/unpaired/random-trigger
samples must not be assumed to be skims of collision Main: identify their actual
parent and retained events. A skim cannot restore discarded events or fields.
Different signal masses/energies are not skim substitutes; lifetime reweighting
requires documented model compatibility, support and validation.

## Required sources

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

Keep required unresolved samples in a separate gaps table: role/point, gap
classification, known parent/source if any, whether a selection could suffice
and evidence still needed, blocker and next action. Write **unresolved** for an
unknown DID; never insert speculative names or wildcard queries. Keep every
required signal point explicit. Consolidate shared unknown-period blockers;
expand periods only when included in the stated scenario.

Classify gaps as: selection on an existing source; unverified retention or
provenance; missing derivation of a known parent; unresolved physics production;
external metadata; or optional scope decision. A failed search alone does not
establish a missing production. GRLs, conditions and joins are dependencies, not
invented event datasets. Keep empty, superseded and unusable sources in a separate
rejected-candidates table; they do not count toward required-source coverage.

Do not collapse necessary slices or signal points into a representative smoke
sample. Shared DIDs cover multiple roles/requirements without duplicate rows.
Reconcile every input requirement using grouped IDs; do not reproduce its full
accessor definition from the upstream contract.

## Overlap audit and evidence

Audit exact DID duplication, container/member overlap, alternative productions of
the same events, overlapping streams, and generator filter partitions separately.
Similar names or a shared EVNT ancestor alone do not prove duplicate reconstructed
samples. Campaigns need an explicit data exposure/pileup mapping. Select one
production per coverage unit unless an evidenced extension or split requires
more. Disjoint decay/filter slices are not duplicates; explain their combination
and normalization rather than merging them by process name.

Store shared recommendation, PMG include-chain and metadata evidence once, with
short IDs in rows. Report distinct provenance per production without repeating
whole metadata dumps or identical generator settings. Checkpoint a compact
manifest early, then refine evidence and blockers as discovery proceeds.

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
