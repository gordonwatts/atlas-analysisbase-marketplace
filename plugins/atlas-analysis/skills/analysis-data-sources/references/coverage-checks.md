# Trigger, signal and raw-input coverage

Use the current analysis specification and supplied mapping/probe inputs. A
technical tier test needs representative collision data and signal simulation;
it does not require a complete physics sample inventory. Start with one file per
probe and retain fail regions. Report a bounded fixture's scope honestly.

For collision triggers execute menu/chain discovery and decision access on the
actual production. Inspect relevant online objects/navigation or offline matching
inputs where required. Separate a chain absent from a menu, present but not fired,
missing retained navigation, accessor/API failure, and service/auth failure.
All-false decisions can prove readability with menu evidence, not efficiency.
When the analysis chain is unresolved, document candidates and their menu evidence;
do not invent an approved chain, tag-only acceptance, plateau or exposure.

For signal truth first derive expected species/PDG IDs, parents and decay modes
from independently checked generator/sample provenance, following executable job
option includes when available. Do not infer the model from a suggestive DID.
Inspect actual returned species and counts, expected particles' four-momenta,
production/decay vertices and units, parent/child link validity, and reconstructed
object matching inputs. Check decay geometry and missing/sentinel values. A generic
nonempty truth collection or SM MC is not evidence for the requested signal.
Do not label every reconstructed object in signal MC as signal. Distinguish
slimmed/missing truth, wrong sample, insufficient coverage and accessor failure;
missing truth is not zero signal efficiency. An evidenced retention gap warrants
a richer-tier test with production provenance, event joins and object matching.
Expected species and required decay details come from the supplied analysis;
LLPs and displaced vertices are not universal requirements for unrelated analyses.

Report production-vertex and decay-vertex validity and geometry separately.
Requiring both before reporting any geometry can hide retained decay positions
when production links were slimmed. Flight length/proper time still needs both.
Truth can be split across retained companion containers: inspect relevant
collections before declaring a tier-wide absence, and use event identity plus
stable particle identifiers, compatible four-momenta and explicit link checks
for any cross-container association. A per-container index is not a global
particle identity. Keep any richer-tier or companion-container join provisional
until overlaps, ambiguities and missing objects have been measured.

Reuse supplied successful queries and helper definitions before rewriting
accessors. When a new collection-valued helper fails translation, separate that
API/code-generation error from retained-content evidence and isolate the return
shape. Preserve the backend's actual tree/column shapes in the output contract;
do not repackage a kinematic smoke tree to make an original-delivery check pass.

Retrieve raw inputs and validity needed to reconstruct the analysis quantities.
For CalRatio this includes calorimeter sampling/energy ingredients and invalid or
non-positive denominators, plus track kinematics, quality/hits, vertex/pile-up
scope and object alignment for the isolation definition. Stored EMFrac and ghost
or PV track counts remain explicit backups until equivalence is established.
Reading these fields does not establish low-EMF calibration, track completeness,
Run 3 quality choices or trigger performance. Do not fill analysis regions as
part of an extraction-only test.

## Machine-readable coverage

An optional supplied acceptance JSON has `schema_version: 1` and `coverage`, an
array of `{id, sample_role, checks: [names...]}`. The ledger's `coverage` array
must contain the same IDs and roles. Each block has `checks`, an object keyed by
the requested names. Each check has `status` (`verified`, `unverified`,
`unavailable`), `probe_ids`, `columns`, and `summary`. For a verified check, each
column is present in a referenced successful ServiceX probe's observations;
the probe's `sample_role` matches the block. Add external provenance probe IDs
separately when relevant; they cannot stand in for event extraction. Unverified
or unavailable checks must explain the blocker and next step. Keep scientific
observations in the probes (actual species/counts, geometry/link checks, menu
and firing counts), not just assertions of success.

The validator's default mode keeps older version-1 ledgers valid. `--acceptance`
requires the declared blocks/checks and rejects unsupported positive claims.
`--require-complete` additionally fails if any requested check is incomplete.
These structural checks do not replace inspecting ROOT values or independently
reviewing expected species and physics equivalence. Return missing coverage
explicitly; never create synthetic deliveries to satisfy a benchmark.

An acceptance block can additionally declare `evidence_rules`, keyed by check
name. `required_columns` lists columns that must be evidenced for that check.
For `kind: expected_particles`, the ledger check must record `expected_pdg_ids`
(signed integer IDs), `expectation_probe_ids` pointing to successful external
source/query records, and the scoped ServiceX observations must contain
`species_counts` keyed by signed PDG ID with a positive integer count for every
expected species. This prevents generic truth or the wrong species from
satisfying a declared signal-species check; review the independent source to
establish that these really are the analysis's expected particles.

The acceptance root can list `artifacts` as relative file paths. Missing or empty
files appear in `missing_coverage` and fail `--require-complete`; the incomplete
ledger itself remains valid. Completeness here is extraction evidence, not
approval of calibrations, production quality or the physics analysis.
