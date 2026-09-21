---
name: servicex-local-wsl2
description: Debug ATLAS ServiceX xAOD transformations locally on Windows by running servicex-local against a WSL2 AnalysisBase environment, with Rucio file download, VOMS checks, release selection, jet smoke tests, and local log inspection.
---

# ServiceX Local on WSL2

Use this skill when a remote ServiceX xAOD/PHYSLITE transform is failing and
the remote log is not available. It runs the same FuncADL xAOD code generation
and science step locally, using a Windows Python process and the `atlas_al9`
WSL2 distro. It is a debugging workflow, not a replacement for the hosted
ServiceX backend.

Read [references/wsl2-runbook.md](references/wsl2-runbook.md) for the complete
commands and smoke-test script. Keep input files, caches, generated code, logs,
and result files outside the repository.

## Required choices

- Use `servicex-local==1.2.1` for this workflow. Keep the version pinned while
  reproducing a failure and record it in the report.
- Use the release-25 xAOD query package (`func_adl_servicex_xaodr25`) for the
  PHYSLITE example.
- Run the science step in WSL2 distro `atlas_al9`.
- By default, resolve the newest stable compatible `25.2` AnalysisBase patch
  with `asetup --stable AnalysisBase,25.2,latest` in a temporary directory.
  Capture and report the exported `AtlasVersion` value (use `env` if shell
  expansion is empty). Treat this as a candidate: compile the generated jet
  query before accepting it. If the candidate has an xAOD API mismatch, step
  back through available stable `25.2` patches until the same query compiles,
  and record both the rejected candidate and the selected version. A
  user-supplied release may override this search, but still must pass setup and
  compile preflight.
- Do not use a Docker image tag as the WSL release. The WSL runner expects a
  distro and an AnalysisBase version.

`local_deliver()` is not the working WSL entry point in
`servicex-local==1.2.1`. It always builds a Docker image name and then passes
that name to the WSL adaptor as though it were a distro. This is tracked in
[ServiceX-Local issue #98](https://github.com/ssl-hep/ServiceX-Local/issues/98).
Assemble the working path yourself with `LocalXAODCodegen`,
`WSL2ScienceImage("atlas_al9", release)`, and `SXLocalAdaptor`, then call
`deliver(..., adaptor=adaptor)` as shown in the runbook.

## Workflow

1. Choose a temporary Windows work directory. It must be visible from WSL as
   `/mnt/<drive>/...`; do not put the downloaded ROOT file in this checkout.
2. In `atlas_al9`, bootstrap ATLAS, set up Rucio, and check the proxy with
   `voms-proxy-info -timeleft`. If it is expired, run
   `voms-proxy-init --voms atlas` and stop if the user certificate is not
   available. Do not claim a download test passed without a non-zero proxy
   lifetime.
3. Download exactly one file from the confirmed MC23 dataset. The file used by
   the smoke test is `mc23_13p6TeV:DAOD_PHYSLITE.50426177._000001.pool.root.1`
   from the dataset
   `mc23_13p6TeV:mc23_13p6TeV.801166.Py8EG_A14NNPDF23LO_jj_JZ1.deriv.DAOD_PHYSLITE.e8514_e8586_s4618_s4619_r17610_r17609_p7266_tid50426177_00`.
   Confirm the downloaded name, size, and Rucio checksum.
4. Build a FuncADL PHYSLITE query that selects jets and extracts `pt` and
   `eta`. Convert `pt` from MeV to GeV in the query. Keep the first run to one
   input file and use a fresh cache or `ignore_local_cache=True`.
5. Assemble the WSL path yourself: create `LocalXAODCodegen`,
   `WSL2ScienceImage("atlas_al9", release)`, and `SXLocalAdaptor`, then call
   the package's `deliver` with that adaptor. Do not replace this with
   `local_deliver()` until issue #98 is fixed; `local_deliver()` constructs a
   Docker image string even for `platform="wsl2"`, while `WSL2ScienceImage`
   expects a WSL distro and an AnalysisBase release.
6. Verify the returned ROOT file with `uproot`: open its `atlas_xaod_tree`
   tree, list its jet branches, and check that it has a positive entry count.
   Report the resolved release, package versions, input path, output path, and
   whether the transform succeeded.
7. If it fails, inspect the generated request directory and its `wsl_log.txt`
   before changing the query. Separate failures in release setup, Rucio/file
   access, code generation, and the science transformation. On the current
   `atlas_al9` aarch64 platform, servicex-local 1.2.1 may leave
   `source x86_64*/setup.sh` in `runner.sh`; if the log ends with that glob
   error after a successful compile, change it to `source aarch64*/setup.sh`
   in the generated temporary runner and rerun the payload. Preserve the log
   and this package workaround when reporting the failure.

## Boundaries

This skill covers local xAOD/PHYSLITE debugging through the WSL2 backend. Use
the general ServiceX skill for hosted delivery, UprootRaw queries, dataset
discovery, or non-WSL platforms. Do not download a whole Rucio dataset when one
file is sufficient to reproduce the problem.
