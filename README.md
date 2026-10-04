# EPIK8S ELI Beamline Helm Chart

This Helm chart deploys the ELI Beamline control system using the [EPIK8S](https://github.com/infn-epics/epik8s-eli) framework. It manages EPICS IOCs, services, and related infrastructure for the ELI-NP facility.

## Features

- **Declarative IOC and service configuration** via `values.yaml`
- **Automatic deployment** of IOCs, gateways, archivers, and supporting services
- **Integration with Phoebus, ChannelFinder, Olog, Save&Restore, and more**
- **Support for NFS and CIFS mounts, secrets, and custom resources**
- **Custom OPI (Operator Interface) integration**

## Structure

- `deploy/values.yaml`: Main configuration file for all IOCs, services, and infrastructure.
- `opi/Launcher.bob`: Main OPI Entry
- Helm templates: Define Kubernetes resources for each IOC and service.

## Configuration

Edit `deploy/values.yaml` to define:

- **Global settings**: `beamline`, `namespace`, `domain`, etc.
- **Services**: Gateways, archiver, console, notebook, alarm server, etc.
- **IOCs**: Each IOC is described with its name, type, chart, parameters, and device-specific settings.
- **NFS/CIFS Mounts**: Define shared storage for data, autosave, and configuration.
- **OPI Integration**: Configure OPI repositories and macros for each device type.

### Example IOC Definition

```yaml
iocs:
  - name: "llrf01"
    asset: "https://confluence.infn.it/x/doKBBg"
    charturl: 'https://baltig.infn.it/epics-containers/ioc-chart.git'
    template:  "libera-llrf"
    devtype: llrf
    devgroup: rf
    iocprefix: "LEL-RF-LLRF03"
    host: "10.16.4.31"
    exec: "start.sh"
```

### Example Service Definition

```yaml
services:
  gateway:
    charturl: 'https://baltig.infn.it/epics-containers/ca-gateway-chart.git'
    ingress:
      enabled: false
    loadbalancer: 10.16.4.202
    replicaCount: 1
    autosync: true
```

## Usage

1. **Clone the repository**  
   ```sh
   git clone https://github.com/infn-epics/epik8s-eli.git
   cd epik8s-eli
   ```

2. **Edit `deploy/values.yaml`**  
   Customize IOCs, services, and infrastructure as needed.

3. **Upgrade **  
   ```sh
   git commit -m "my changes comments ..." ... 
   git push
   ## synchronize ArgoCD 
   ```

4. **Monitor deployment**  
   Use `kubectl` to check the status of pods and services.

## Documentation & Support

- [Latest Release Notes](https://github.com/infn-epics/epik8s-eli/releases/latest)
- [EPIK8S Documentation](https://github.com/infn-epics/epik8s-eli)
- For internal assets and device documentation, see the `asset` links in `values.yaml`.

---

*This chart is intended for use by ELI-NP controls and operations teams. For questions or contributions, please open an issue or pull request on GitHub.*

