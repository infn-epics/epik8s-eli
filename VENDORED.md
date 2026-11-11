# Vendored sources

This repo used git submodules for the OPIs (`opi/`, formerly the eli-epics-opi
repo) and for some IOC scripts. Many lived on baltig.infn.it, which the ELI
cluster cannot reach, and a single unreachable submodule broke every console
and IOC init clone. They are now plain directories, copied from the commits
the submodules pinned on 2026-11-11 (history not carried over).

To pick up an upstream fix, copy the files from the source repo and update the
commit below. Do not reintroduce submodules.

## Copied in

| Path | Source | Commit |
|---|---|---|
| `config/iocs/orbit/scripts` | https://baltig.infn.it/infn-epics/py-ioc-collector.git | `645a01da4a` |
| `opi/ansible/ansible-epics-console-role` | https://baltig.infn.it/lnf-da-control/ansible-epics-console-role.git | `97ac2c4cc0` |
| `opi/common/camera` | https://baltig.infn.it/infn-epics/camera-opi.git | `8e027d3f61` |
| `opi/common/motor-tml` | https://baltig.infn.it/infn-epics/motor-tml-opi.git | `f8bdcb8ab8` |
| `opi/diag/libera-bpm-opi` | https://baltig.infn.it/infn-epics/libera-bpm-opi.git | `7623301fcb` |
| `opi/epik8s-opi/screen-camera-opi` | ../screen-camera-opi.git | `a77b4c7647` |
| `opi/epik8s-opi/unibpm-opi` | https://github.com/infn-epics/unibpm-opi.git | `c9b45057f8` |
| `opi/epik8s-opi/unicam-opi` | ../unicam-opi.git | `a1961335c7` |
| `opi/epik8s-opi/unicool-opi` | ../unicool-opi | `39745124cb` |
| `opi/epik8s-opi/uniio-opi/icpdas-opi` | ../icpdas-opi.git | `813f50c820` |
| `opi/epik8s-opi/uniio-opi` | ../uniio-opi.git | `0af491d389` |
| `opi/epik8s-opi/unimag-opi` | ../unimag-opi | `8a4a131424` |
| `opi/epik8s-opi/unimod-opi/scandinova-opi` | https://github.com/infn-epics/scandinova-opi.git | `8b6fe86783` |
| `opi/epik8s-opi/unimot-opi` | ../unimot-opi | `c16d6f2df5` |
| `opi/epik8s-opi/univac-opi` | ../univac-opi | `1ba55e842a` |
| `opi/epik8s-opi` | https://github.com/infn-epics/epik8s-opi.git | `4cf9da800c` |
| `opi/RF/eli-rf-opi` | https://github.com/infn-epics/eli-rf-opi.git | `0ce4812638` |
| `opi/RF/menloOpi` | https://baltig.infn.it/infn-epics/menloOpi.git | `6c571889b7` |
| `opi/timing/mrf230-opi` | https://baltig.infn.it/infn-epics/mrf230-opi.git | `709c9421f6` |
| `opi/VAC/vac-opi` | https://baltig.infn.it/infn-epics/vac-opi.git | `4e49ffbaec` |
| `opi` | ../eli-epics-opi.git | `ee77ccc5c7` |

Relative sources (`../name`) resolve against the parent repo's remote, e.g.
`opi/epik8s-opi/unimag-opi` came from https://github.com/infn-epics/unimag-opi.

Local changes made while copying:
- `opi/ansible/ansible-epics-console-role/defaults/main.yml`: the hard-coded
  `git_repo_token` was blanked; the playbooks pass it from `GIT_REPO_TOKEN`.
- `opi/MAG/polarityreversal.bob`: links to `common/icpdas-opi` now point at
  `epik8s-opi/uniio-opi/icpdas-opi` (newer copy of the same repo).

## Dropped (not referenced by ELI screens or IOCs)

| Path | Source | Last pinned commit |
|---|---|---|
| `opi/common/icpdas-opi` | https://baltig.infn.it/infn-epics/icpdas-opi.git | `15280dc001` |
| `opi/diag/orbit` | https://baltig.infn.it/lnf-da-control/epics-orbit-opi.git | `79c6001710` |
| `opi/MAG/mag-opi` | https://baltig.infn.it/infn-epics/mag-opi.git | `fb321d45d6` |
| `opi/MAG/unimag` | https://baltig.infn.it/infn-epics/unimag.git | `e864527e19` |
| `opi/matlab-routines/matlab_sparcroutines` | https://baltig.infn.it/pompilir/matlab_sparcroutines.git | `2a75f4e623` |
| `opi/rp-opi` | https://baltig.infn.it/lnf-da-control/redpitaya-ioc.git | `c5663f42e7` |
| `opi/timing/phoebus_mrf_interface` | https://baltig.infn.it/lnf-da-control/phoebus_mrf_interface.git | `d4b52ab3db` |
| `config/iocs/klyloop/scripts` | https://baltig.infn.it/lnf-da-control/klystron-loop-soft-ioc.git | `6d84bbef50` |
| `config/iocs/lasersynch/scripts` | https://baltig.infn.it/lnf-da-control/laser-synch-soft-ioc | `3e682a05af` |
| `config/iocs/mem2epics/scripts` | https://baltig.infn.it/infn-epics/memcached2epics.git | (not pinned) |
| `config/iocs/mag-wrapper/scripts` | https://baltig.infn.it/lnf-da-control/softioc-devil-wrapper-for-sparc.git | (not pinned) |

`common/icpdas-opi` is still available at `opi/epik8s-opi/uniio-opi/icpdas-opi`.
