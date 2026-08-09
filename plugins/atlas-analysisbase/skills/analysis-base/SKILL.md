---
name: analysis-base
description: Create and configure CERN ATLAS AnalysisBase work areas, CPRun PHYSLITE or DAOD inputs, C++ AnaAlgorithms with systematic-aware outputs, small-R jet uncertainties, ntuple dumper variables, builds, and smoke tests. Use for new AnalysisBase areas, custom algorithms, CP systematics, or AnalysisBase setup and run instructions.
---

# AnalysisBase

Build reproducible ATLAS AnalysisBase analyses with `CPRun.py`. Read
`references/analysis-base-reference.md` for the compact C++ and YAML patterns.

## Setup

Inspect the requested release, input format, CVMFS availability, and platform;
never assume `x86_64`. For the validated setup use `AnalysisBase,25.2.73` and
the generated platform directory, commonly `aarch64-el9-gcc14-opt`.

Create or preserve the work area, add packages under `source/`, then build:

```bash
source /cvmfs/atlas.cern.ch/repo/sw/software/25.2/AnalysisBase/25.2.73/InstallArea/<platform>/setup.sh
cd AnalysisTutorial/build
cmake ../source
cmake --build . --parallel "$(nproc)"
source ../build/<platform>/setup.sh
```

On hosts where the factory scanner loads the wrong C++ runtime, prepend the
release GCC `lib64` directory to `LD_LIBRARY_PATH` before building or running.

## Common CP systematics

For full configured systematics, set:

```yaml
CommonServices:
  runSystematics: true
  enableExpertMode: true
```

Remove any `filterSystematics`. “Full” means all variations registered by the
configured CP blocks. For small-R `AntiKt4EMPFlowJets`, add the uncertainty
block inside the corresponding `Jets` entry:

```yaml
Uncertainties:
- containerName: AnaJets
  jetInput: EMPFlow
```

This creates the JES/JER jet-container variations that a jet algorithm can
read. For the tested PHYSLITE Run-2 YAML also keep the output commands that
disable unavailable `actualInteractionsPerCrossing` and
`tau_passTATTauMuonOLR` decorations.

## Custom systematic-aware algorithms

Use a C++ `EL::AnaAlgorithm` with `CP::SysListHandle`,
`CP::SysReadHandle<T>`, and `CP::SysWriteDecorHandle<T>`. Initialize the
handles, loop over `m_systematicsList.systematicsVector()`, retrieve the
variation with the active release API, calculate from that variation, and
write a `%SYS%` decoration. In AnalysisBase 25.2.73 the jet read pattern is:

```cpp
const xAOD::JetContainer* jets = nullptr;
ANA_CHECK (m_jets.retrieve (jets, sys));
for (const xAOD::Jet* jet : *jets) {
  m_output.set (*jet, calculate (*jet), sys);
  m_output.lock (*jet, sys);
}
```

Register the component with `DECLARE_COMPONENT` and
`AsgTools/AsgComponentFactories.h`; link the package library against
`AnaAlgorithmLib`, `SystematicsHandlesLib`, and the object library it reads.

## Scheduling and ntuple output

Plain CPRun YAML does not schedule arbitrary user components. Add a Python
`ConfigBlock` through `AddConfigBlocks`; its `makeAlgs` must call
`config.createAlgorithm`, set the systematic input name with
`config.readName(...)`, and call:

```python
config.addOutputVar(containerName, "myVariable_%SYS%", "myVariable")
```

Add a top-level YAML instance for the block, for example
`GordonsPT: {containerName: AnaJets}`. Insert the block at `pos: Thinning` when
the ntuple maps `jet_` to `OutJets`, so the decoration is copied into the
output container before thinning. Keep `%SYS%` and `noSys: false` for values
that vary with systematics.

## Validate

Validate the input with `checkxAOD.py` and a ROOT `CollectionTree` check. Run a
short smoke test before a full sample:

```bash
runPHYSLITEAnalysis "$ALRB_Test_File" 5 2>&1 | tee smoke.log
```

Confirm CPRun reports `runSystematics: True`, the worker succeeds, `output.root`
contains an `analysis` tree, and the tree has nominal and representative
up/down output branches. For a derived jet variable, compare each output
branch to the corresponding systematic jet input branch. Do not start an
all-events run without estimating its cost.

Preserve existing work, use `apply_patch` for edits, rerun CMake after adding
files, and record release-specific gaps when the user requests durable notes.
