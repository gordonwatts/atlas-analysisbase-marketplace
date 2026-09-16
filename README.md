# Codex ATLAS Analysis Workspace

This repository packages the `atlas-analysis` Codex plugin. It is the
ATLAS-specific workspace for skills that support a complete, reproducible
analysis workflow. The first skill is `analysis-base`, covering CERN ATLAS
AnalysisBase work areas, systematic-aware C++ algorithms, small-R jet
uncertainties, CPRun, and ntuple dumper output.

The workspace is intentionally organized as one plugin with multiple focused
skills. Additional analysis stages will be added only after their guidance has
been tested and reviewed. Each skill should document the tools and decision
points specific to its stage of the workflow; do not duplicate generic ATLAS
or Python guidance.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/atlas-analysis/
└── skills/analysis-base/
```

## Use locally in Codex

From this repository:

```bash
codex plugin marketplace add "$PWD"
codex plugin add atlas-analysis@personal
```

Start a new Codex thread after installation so the updated skill is loaded.

## Publish on GitHub

Create an empty GitHub repository, then run:

```bash
git remote add origin git@github.com:<OWNER>/codex-atlas-marketplace.git
git push -u origin main
```

Clone that repository wherever Codex runs, add the clone as a marketplace with
`codex plugin marketplace add /path/to/codex-atlas-marketplace`, and install
`atlas-analysis@personal`.

The repository intentionally contains the user-owned `analysis-base` skill;
Codex system and curated skills are not redistributed.

## Test Prompts

Below are some of the prompts used to test this still (sub-prompts means one prompt built on the previous prompts).

* Using the `analysis-base` skill from `atlas-analysis`, please build from scratch an AnalysisBase config file that you run that only dumps out the jet pt, eta, and phi. Run on 100 events from the tutorial's PHYSLITE file, and call the output file ab-ntuple.root. Report back the size of the file and how many jets are in it. Finally, list anything that should have been in the analysis base skill that would have helped you complete this job more efficiently.
  * Now that a simple run for 100 events with no systematics is done, create a new output file (ab-ntuple-sys.root) that contains a run with systematics. Configure the system to just run the jet systematics. There are so many of them and they are expensive, so we want to run efficiently - we just need the jet variations.
  * Now that a run with just jet systematics is working, please create a new AnalysisBase algorithm that reads in the jet pt, eta, and phi. It then Writes out a pt*2, eta, and phi (doubles the pt). It should correctly participate in the systematic error loop. The output dumper should dump the raw jet pt, eta, phi as it does now, as well as the three from the new package (and all their systematic variations). When you are done, please look back over your work and see if there is anything that would have helped you get to the answer more quickly if it was in the skill.
