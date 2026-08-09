# Codex ATLAS Marketplace

This repository packages the `atlas-analysisbase` Codex plugin. It contains
the updated `analysis-base` skill for CERN ATLAS AnalysisBase work areas,
systematic-aware C++ algorithms, small-R jet uncertainties, CPRun, and ntuple
dumper output.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/atlas-analysisbase/
└── skills/analysis-base/
```

## Use locally in Codex

From this repository:

```bash
codex plugin marketplace add "$PWD"
codex plugin add atlas-analysisbase@personal
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
`atlas-analysisbase@personal`.

The repository intentionally contains the user-owned `analysis-base` skill;
Codex system and curated skills are not redistributed.
