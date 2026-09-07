---
name: analysis-base
description: Create and configure CERN ATLAS AnalysisBase work areas, CPRun PHYSLITE or DAOD inputs, C++ AnaAlgorithms with systematic-aware outputs, small-R jet uncertainties, ntuple dumper variables, builds, and smoke tests. Use for new AnalysisBase areas, custom algorithms, CP systematics, or AnalysisBase setup and run instructions.
---

# AnalysisBase

AnalysisBase (AB) is the general ATLAS analysis framework, used by physicists to access almost all analysis data formats (derivations like DAOD_PHYSLITE, DAOD_PHYS, DAOD_LLP1, etc). It is a C++ framework with Python steering, and it is built on top of the EventLoop framework. It provides a set of common tools for physics analysis, including systematic uncertainty handling, jet calibration, and more. The framework is driven by a YAML configuration file, which specifies the input data, algorithms to run, and output formats. You can add custom algorithms to dump variables not supported by default (or calculate derived quantities).

- Create, build, and configure custom AB algorithms - read the skill reference file `references/analysis-base-reference.md`

Below are instructions for basic running. If you only need the standard output variables (associated with any object like jets, electrons, muons, etc), you can skip the custom algorithm steps and just use the standard configuration files.

This skill when it uses the word `container` means a data container, for example, the jet collection is in the jet container. If you are looking for the jet pt (transverse momentum), then it is going to be in the jet container.

## Mandatory Environment Setup

You'll need to setup the shell's environment with the release before working. Once that is done, you'll need to build any packages you create.

You _must_ setup the environment before running any of the tools using the below lines. You must always use the native host shell (or invoke bash, etc.). Never run anything in a container.

The following lines, at the top of a script (or via the shell) will setup AnalysisBase release 25.2.73. You should assume
you are running on a well configured machine with `cvmfs`. If that first `source` fails because that file can't be found,
then you should report the error back to the user: the machine you are running on is not configured and the user must
move to another machine. If the `asetup` fails, then that is because the release is missing - you may have to search for other releases.

For the tutorial validated setup use `AnalysisBase,25.2.73` - the user may need to operate in a different release, of course.

```sh
# The ATLAS setup scripts require unset variables to be allowed
set +e +u +o pipefail
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
asetup AnalysisBase,25.2.73
set -euo pipefail
```

You'll need to do this only once (or inside a script that requires it).

## Directory Layout

Build directory with the following structure:

- `source` Put top level CMakeLists.txt and other source files here. Your configuration `yaml` file should go here as well. If you create any new analysis packages (or check them out) they will be placed under this `source` directory.

* `build`: This is where all the files created by the build system go. If you build a custom algoirthm, this is where the output of the `cmake` command will go.

* `run`: This is where you actually run your programs, collect your output files, etc. For example, output root files will be written here. You can also put your input files here, or you can point to them in a different location.

## `yaml` configuration

AnalysisBase is steered by a YAML configuration file. The `CPRun.py` entry point reads the YAML, creates the requested algorithms, and schedules them with the configured input and output.

Example configuration files for Run 2 and Run 3 processing can be found in `$AnalysisBase_DIR/src/PhysicsAnalysis/Algorithms/AnalysisAlgorithmsConfig/data` ($AnalysisBase_DIR is defined after the `asetup` command).

### Output variables

Here is an example output block that will write out all the EventInfo variables with a `evt_` prefix:

```
# Specify the name of the output tree and any variables associated
# with a container to save. Only write out the EventInfo container variables
Output:
    treeName: 'analysis'
    # Variables associated with containers other than MET
    #   Syntax without systematics: '<Container>_NOSYS -> <branch name>'
    #   Syntax with systematics: '<Container>_%SYS% -> <branch name>'
    vars: []
    containers:
        'evt_': 'EventInfo'
```

The `Output.commands` part of the config file accepts regular-expression patterns for selecting output
variables to disable. This applies to variables produced by any configured
container or algorithm block. Note that by default only the basics are dumped. See example file above for syntax.

Variables registered by a standard block with `noSys=True` remain nominal-only
even when `runSystematics: true`. If the producing algorithm decorates a
systematic container and one branch per variation is required, add an explicit
`Output.vars` mapping whose source and destination use `%SYS%`, then verify the
expanded branch names in the ROOT tree.

Use anchors when disabling one exact variable:

```yaml
Output:
  commands:
    - disable ^jet_e$
```

Here ^jet_e$ matches only jet_e. An unanchored pattern such as jet_e
may also match longer output names containing that substring. Standard
variables can be added automatically by an output container mapping, so check
the CPRun configuration log and resulting tree when an unexpected variable
appears.

### Common CP systematics

Systematics are very expensive to run. Do not run them unless the user asks for them explicitly.

For full configured systematics, set:

```yaml
CommonServices:
  runSystematics: true
```

Add `   filterSystematics: '^(?:(?!PseudoData).)*$'` under `CommonServices` to use a regex to filter out only the systematics you want to run. Without it you'll run all systematic errors ("Full").

For small-R `AntiKt4EMPFlowJets`, add the uncertainty
block inside the corresponding `Jets` entry in your yaml file:

```yaml
Uncertainties:
  - containerName: AnaJets
    jetInput: EMPFlow
```

This creates the JES/JER jet-container variations that a jet algorithm can
read. Output command patterns fail when they match no scheduled branch. For
release- or configuration-dependent exclusions, use `optional disable`; for
example, the tested PHYSLITE Run-2 YAML may need:

```yaml
Output:
  commands:
    - optional disable actualInteractionsPerCrossing
    - optional disable tau_passTATTauMuonOLR
```

When running, check the log for a list of all the systematics to make sure the exected ones are running. Systematics are very CPU intensive - so it is very worth running a 5 event smoke test to make expected systematics are running.

## Validate

Validate the input with `checkxAOD.py` and a ROOT `CollectionTree` check. Run a
short smoke test before a full sample:

Run a short smoke test with the standard `CPRun.py` entry point. Run from the
`run` directory and pass a basename such as `output.root` to `-o`; absolute or
prefixed paths can be resolved inside EventLoop's worker staging area instead
of at the intended destination. The `-e 5` limits processing to five events,
which is useful for a smoke test.

```bash
printf '%s\n' "$ALRB_Test_File" > input.txt
CPRun.py -i input.txt -t config.yaml -o output.root -e 5 2>&1 | tee smoke.log
```

Confirm CPRun reports the requested systematics mode, the worker succeeds, and
the final ROOT file contains the expected tree and branches. EventLoop may
stage or fetch the tuple below its work directory before producing a merged
top-level file, so do not assume a fixed `workDir/data-<streamName>/` path;
locate and validate the actual output after worker success. When systematics
are requested, inspect nominal and representative up/down branches. For a
derived variable, compare each output branch to the corresponding systematic
input branch. Remember that `-e N` limits processed events while configured
filters can reduce the retained tree entries. Do not start an all-events run
without estimating its cost.

Preserve existing work, use `apply_patch` for edits, rerun CMake after adding
files, and record release-specific gaps when the user requests durable notes.
If a run script uses `set -u`, temporarily disable nounset while sourcing the
generated `build/<platform>/setup.sh`, then restore it before running the job;
generated setup scripts may reference optional package variables that are unset.
