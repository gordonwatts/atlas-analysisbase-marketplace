# ATLAS Analysis

This repository packages the `atlas-analysis` plugin. It is the
ATLAS-specific workspace for skills that support a complete, reproducible
analysis workflow.

The plugin currently provides:

- `analysis-base`: CERN ATLAS AnalysisBase work areas, systematic-aware C++
  algorithms, small-R jet uncertainties, CPRun, and ntuple dumper output.
- `find-atlas-datasets`: centrally produced MC sample discovery with AMI
  metadata and provenance checks, plus executable PMG job-options verification.

The workspace is intentionally organized as one plugin with multiple focused
skills. Additional analysis stages will be added only after their guidance has
been tested and reviewed. Each skill should document the tools and decision
points specific to its stage of the workflow; do not duplicate generic ATLAS
or Python guidance.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/atlas-analysis/
└── skills/
    ├── analysis-base/
    └── find-atlas-datasets/
```

## Use locally in Codex

From this repository:

```bash
codex plugin marketplace add "$PWD"
codex plugin add atlas-analysis@personal
```

Start a new Codex thread after installation so the updated skill is loaded.

Invoke a skill explicitly with its name, for example:

```text
Use $find-atlas-datasets to find MC23 samples for <physics request>.
```

The dataset skill reports the catalog search terms and failed routes, candidate
dataset metadata, the EVNT-to-derivation provenance chain, the PMG include chain,
and a confidence label that distinguishes executable job-options evidence from
AMI-only or incomplete matches.

## Test Prompts

Below are some of the prompts used to test this still (sub-prompts means one prompt built on the previous prompts).

- Using the `analysis-base` skill from `atlas-analysis`, please build from scratch an AnalysisBase config file that you run that only dumps out the jet pt, eta, and phi. Run on 100 events from the tutorial's PHYSLITE file, and call the output file ab-ntuple.root. Report back the size of the file and how many jets are in it. Finally, list anything that should have been in the analysis base skill that would have helped you complete this job more efficiently.
  - Now that a simple run for 100 events with no systematics is done, create a new output file (ab-ntuple-sys.root) that contains a run with systematics. Configure the system to just run the jet systematics. There are so many of them and they are expensive, so we want to run efficiently - we just need the jet variations.
  - Now that a run with just jet systematics is working, please create a new AnalysisBase algorithm that reads in the jet pt, eta, and phi. It then Writes out a pt*2, eta, and phi (doubles the pt). It should correctly participate in the systematic error loop. The output dumper should dump the raw jet pt, eta, phi as it does now, as well as the three from the new package (and all their systematic variations). When you are done, please look back over your work and see if there is anything that would have helped you get to the answer more quickly if it was in the skill.
