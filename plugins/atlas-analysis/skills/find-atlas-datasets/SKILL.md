---
name: find-atlas-datasets
description: Find centrally produced ATLAS MC EVNT datasets for a physics process and campaign, verify AMI provenance and PMG job options, and report the evidence for each match. Use for MC sample discovery, DSID verification, or EVNT-to-derivation tracing. Finds only the MC EVNT records.
---

# Find ATLAS datasets

Use this skill for a request containing a physics concept (for example, ttbar or jets), a run or MC campaign, and optional process, decay, generator, or derivation constraints. Return candidates with enough evidence to distinguish the generated physics from a suggestive dataset name. Keep this a read-only discovery workflow.

## Discover candidates

1. Translate the request into catalog-visible tokens and synonyms that can be used to search AMI in step 2. Use the atlas-af MCP Atlas Search service, when available, to discover vocabulary from the physics description; record the actual terms tried. If it is unavailable or lacks coverage, use other authoritative ATLAS sources and say so. Resolve the requested run to the appropriate MC campaign and AMI catalog; check the catalog rather than assuming its name from the LDN. For example, an MC23 LDN can begin mc23_13p6TeV while the catalog is mc23_001:production. Only scopes that start with `mc` or `data` are valid, unless explicitly requested otherwise.

2. Search AMI EVNT records first. Try, in order when applicable: exact DSID; exact or wildcard physicsShort; generator and physics tokens; logical dataset name where supported; then PMG hashtags. Use direct AMI queries when a specialized helper returns no results. An empty hashtag result does not establish absence. Keep unsuccessful query routes in the search record.

3. For each plausible EVNT candidate, use AMI parent/child and task provenance to trace simulation, reconstruction, and the requested DAOD derivation. Verify the actual parent EVNT rather than matching descendants by DSID or name alone. Use Rucio read-only DID queries to corroborate existence or counts when useful; do not substitute them for AMI provenance.

## Verify each candidate

Retrieve and record, where available, the full LDN, DSID, campaign, collision energy, data type and derivation, event and file counts, status, cross-section and filter efficiency, generator, tune, PDF, Athena release, physics description, keywords, process metadata, parent EVNT, and the simulation/reconstruction/derivation chain. Preserve values and units as reported. Mark a missing field as unavailable instead of filling it from the name or a related production. Do not classify the generated process solely from physicsShort or the LDN.

Inspect the [official PMG MCJobOptions repository](https://gitlab.cern.ch/atlas-physics/pmg/mcjoboptions) for every candidate DSID at `<first-three-digits>xxx/<DSID>/` (for example, 537xxx/537840/). Read every .py file in that DSID directory. Follow every include(...) statement, including relative includes, until the shared executable implementation is reached; record the exact path chain. Use direct GitLab browsing or a read-only clone if needed. Atlas Search may not index this repository: an empty exact DSID or filename search is a search-index limitation, not evidence that job options are absent.

Extract the executable MadGraph model, process and decay chain, mass and width parameters, lifetime implementation, generator filters, run-card and parameter-card settings, Pythia8 commands and tune, and evgenConfig description and keywords. Prefer executed process strings and assignments over comments, which may be stale. Distinguish a complete static card from a wrapper around shared fragments and from Python that generates proc_card, run_card, or param_card at runtime. For runtime cards, name the generating functions and identify the EVGEN job log or working-directory output as the source of the concrete cards. Do not attribute detector simulation, reconstruction, or derivation settings to EVGEN job options; use AMI task metadata and log datasets for those stages.

## Report

- Give a candidate table with DSID, full LDN, campaign, match status, and one of these confidence labels: **Confirmed by executable job options**, **Confirmed by AMI metadata only**, or **Plausible but not fully verified**. Only report back the EVNT file - the specific derivation will be decided later in the workflow.
- For each candidate, briefly interpret the physics and cite the exact PMG files and include chain supporting its model, process, decay, masses, lifetime, filters, and generator settings. Separate observed configuration from inference.
- Show the AMI provenance chain from EVNT through the requested derivation, with direct GitLab file links and AMI identifiers or links where available. Include key metadata and explicitly identify unavailable fields or unverified links.
- List the search terms and routes tried. Explain failed searches, including catalog naming, missing metadata or hashtags, access limits, and Atlas Search index coverage as applicable. If no match is found, report the attempted routes and the remaining uncertainty; do not claim that a sample does not exist solely from empty search results.
