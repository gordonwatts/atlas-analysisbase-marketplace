# AnalysisBase Custom Packages

There are several steps to scaffold a custom package.

If creating from scratch, create a new directory with the package name in your `source` directory. We'll call it `MyAnalysis` for this. Then inside this directory you'll need to create the following sub-directories:

* `MyAnalysis`: This is where all of your (public) C++ header files go. By ATLAS convention it is always named the same as the package itself.

* Root: This is where most of your C++ source files go, as well as any private header files.

* `src`: This is where Athena-specific C++ source files and private header files go. Generally, files in Root are visible in both Athena and AnalysisBase, while files in src are only visible in Athena. If this is an AB only package, create the directory by convention.

* `share`: This is where configuration and small data files go that you need to pick up at run time.

* `python`: This is where python modules go. In particular, files here are used to schedule predefined algorithms that should be executed in addition to your analysis algorithm.

## Package skeleton

Keep the work-area project and each package in separate CMake layers. The
top-level `source/CMakeLists.txt` should contain the project setup, including a
version for `atlas_project`:

```cmake
cmake_minimum_required(VERSION 3.14 FATAL_ERROR)
project(MyAnalysisProject VERSION 1.0.0)

find_package(AnalysisBase REQUIRED)
atlas_project(USE AnalysisBase "${AnalysisBase_VERSION}")
```

Put the following package-level `CMakeLists.txt` in
`source/MyAnalysis/CMakeLists.txt`, alongside the package directories. Do not
put `atlas_subdir` or package targets in the top-level project file:

```cmake
atlas_subdir( MyAnalysis )

atlas_add_library( MyAnalysisLib
  MyAnalysis/*.h Root/*.cxx
  PUBLIC_HEADERS MyAnalysis
  LINK_LIBRARIES AnaAlgorithmLib SystematicsHandlesLib xAODJet )

atlas_add_component( MyAnalysis
  src/components/*.cxx
  LINK_LIBRARIES MyAnalysisLib )

atlas_install_python_modules( python/*.py )
atlas_install_data( data/*.yaml )
```

Register the component with `DECLARE_COMPONENT` and
`AsgTools/AsgComponentFactories.h`; link the package library against
`AnaAlgorithmLib`, `SystematicsHandlesLib`, and the object library it reads. This should be in `MyAnalysis/src/components/MyAnalysis_entries.cxx`.

```cpp
#include "MyAnalysis/MyAlgorithm.h"
#include "AsgTools/AsgComponentFactories.h"
DECLARE_COMPONENT (MyAnalysis::MyAlgorithm)
```

## Building Custom Packages

Add packages under `source/`, and create a `build` area to build in:

```bash
cd AnalysisTutorial/build
cmake ../source
cmake --build . --parallel "$(nproc)"
source ../build/<platform>/setup.sh
```

## Systematic-aware algorithm

To make the algorithm systematics aware you'll need to add a few other things:

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

```cpp
#include <AnaAlgorithm/AnaAlgorithm.h>
#include <SystematicsHandles/SysListHandle.h>
#include <SystematicsHandles/SysReadHandle.h>
#include <SystematicsHandles/SysWriteDecorHandle.h>
#include <xAODJet/JetContainer.h>

CP::SysListHandle m_systematicsList {this};
CP::SysReadHandle<xAOD::JetContainer> m_jets {
  this, "jets", "", "systematic-dependent jets"};
CP::SysWriteDecorHandle<float> m_output {
  this, "myVariable", "myVariable_%SYS%", "systematic-dependent output"};
```

Initialize and execute with the release-compatible read API:

```cpp
ANA_CHECK (m_jets.initialize (m_systematicsList));
ANA_CHECK (m_output.initialize (m_systematicsList, m_jets));
ANA_CHECK (m_systematicsList.initialize ());

for (const auto& sys : m_systematicsList.systematicsVector()) {
  const xAOD::JetContainer* jets = nullptr;
  ANA_CHECK (m_jets.retrieve (jets, sys));
  for (const xAOD::Jet* jet : *jets) {
    m_output.set (*jet, calculate (*jet), sys);
    m_output.lock (*jet, sys);
  }
}
```

Use the corresponding systematic object and `%SYS%` decoration for other
container types. Do not write all variations into one fixed decoration.

## CPRun configuration and ntuple output

Plain CPRun YAML does not schedule arbitrary user components. Register a Python
`ConfigBlock` factory and instantiate it in YAML. `modulePath` is the installed
module path; modules installed by an ATLAS package are normally package-qualified:

```yaml
AddConfigBlocks:
- modulePath: MyAnalysis.MyConfig
  functionName: MyConfig
  algName: MyAlgorithm
  pos: Thinning

MyAlgorithm:
  containerName: AnaJets
```

The factory must accept the configuration sequence and append the block;
returning a block from a zero-argument function is not sufficient in
AnalysisBase 25.2.x. Declare user-settable values with `addOption`; values are
supplied in the separate root YAML stanza named by `algName`. The block creates
the component and registers its output:

```python
from AnalysisAlgorithmsConfig.ConfigBlock import ConfigBlock


class MyConfigBlock(ConfigBlock):
    def __init__(self):
        super().__init__()
        self.addOption("containerName", "", type=str)

    def makeAlgs(self, config):
        alg = config.createAlgorithm(
            "MyAnalysis::MyAlgorithm", "MyAlgorithm_" + self.containerName)
        alg.jets = config.readName(self.containerName)
        config.addOutputVar(
            self.containerName, "myVariable_%SYS%", "myVariable")


def MyConfig(seq):
    seq.append(MyConfigBlock())
```

When `Output` maps `jet_` to `OutJets`, place the block before `Thinning` so
the decoration is copied into `OutJets` before the ntuple maker runs. Keep
`noSys` false for systematic-dependent values.

## Smoke test

Use the fixed PHYSLITE tutorial input when applicable:

```bash
export ALRB_TutorialData=/cvmfs/atlas.cern.ch/repo/tutorials/asg/cern-mar2025
export ALRB_Test_File="$ALRB_TutorialData/mc20_13TeV.312276.aMcAtNloPy8EG_A14N30NLO_LQd_mu_ld_0p3_beta_0p5_2ndG_M1000.deriv.DAOD_PHYSLITE.e7587_a907_r14861_p6117/DAOD_PHYSLITE.37791038._000001.pool.root.1"
CPRun.py "$ALRB_Test_File" 5 2>&1 | tee smoke.log
```

Check `output.root`, the `analysis` tree, `runSystematics: True`, worker
success, and nominal/up/down branches. For a derived jet value, verify each
output branch against the matching systematic `jet_pt` branch.

