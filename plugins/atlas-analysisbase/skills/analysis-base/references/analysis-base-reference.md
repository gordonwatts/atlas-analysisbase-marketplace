# AnalysisBase reference

Validated with `AnalysisBase,25.2.73` on `aarch64-el9-gcc14-opt`. Check the
release and generated platform before using these examples.

## Package skeleton

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

Register components with the active factory header:

```cpp
#include "MyAnalysis/MyAlgorithm.h"
#include "AsgTools/AsgComponentFactories.h"
DECLARE_COMPONENT (MyAnalysis::MyAlgorithm)
```

## Systematic-aware algorithm

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

Plain CPRun YAML does not schedule arbitrary user components. Import a Python
`ConfigBlock` and instantiate it in YAML:

```yaml
AddConfigBlocks:
- modulePath: MyAnalysis.MyConfig
  functionName: MyConfig
  algName: MyAlgorithm
  pos: Thinning

MyAlgorithm:
  containerName: AnaJets
```

The installed module path follows the package layout under `python/`; for
example `python/MyAnalysis/MyConfig.py` installs as `MyAnalysis.MyConfig`.
The block must create the component and register its output:

```python
def makeAlgs(self, config):
    alg = config.createAlgorithm(
        "MyAnalysis::MyAlgorithm", "MyAlgorithm_" + self.containerName)
    alg.jets = config.readName(self.containerName)
    config.addOutputVar(
        self.containerName, "myVariable_%SYS%", "myVariable")
```

When `Output` maps `jet_` to `OutJets`, place the block before `Thinning` so
the decoration is copied into `OutJets` before the ntuple maker runs. Keep
`noSys` false for systematic-dependent values.

## Jet systematics

For small-R `AntiKt4EMPFlowJets`, put this inside the matching `Jets` entry:

```yaml
Uncertainties:
- containerName: AnaJets
  jetInput: EMPFlow
```

With `CommonServices.runSystematics: true` and no filter, this produces the
JES/JER variations consumed by the systematic read handle.

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
