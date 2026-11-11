ansible-epics-console-role
=========

Ansible role to install and configure Phoebus EPICS console on Ubuntu machines.

This role:
- Installs Java (17 or 21)
- Downloads and installs Phoebus from GitHub releases or binary server
- Configures OPI repositories
- Sets up desktop shortcuts
- Configures proxy settings
- Mounts NFS shares (optional)

Requirements
------------

- Ubuntu/Debian based system
- Ansible 2.9 or higher
- Internet access (or accessible binary server)

Role Variables
--------------

### Phoebus Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `phoebus_version` | `4.7.4-INFN` | Phoebus version tag |
| `phoebus_url` | `""` | Override download URL (auto-detected if empty) |
| `phoebus_home` | `/phoebus` | Installation directory |
| `java_version` | `"21"` | Java version (17 or 21) |
| `install_phoebus` | `true` | Whether to install Phoebus |

### Download URL Auto-Detection

If `phoebus_url` is not set, the role automatically chooses the download source:

- **GitHub Releases**: For versions matching `vX.X.X` pattern (e.g., `v26.2.13b1`)
  - URL format: `https://github.com/infn-epics/phoebus/releases/download/{version}/phoebus-5.0.3-SNAPSHOT-linux.tar.gz`
  
- **Binary Server**: For other version formats (e.g., `4.7.4-INFN`)
  - URL format: `https://opensource.lnf.infn.it/binary/epics/phoebus/linux/product-{version}.tar.gz`

### OPI Configuration

| Variable | Description |
|----------|-------------|
| `opi_repos` | List of OPI git repositories to clone |
| `opi_main` | Default OPI file to launch |
| `opi_path` | OPI installation path |
| `control_user` | User who will run Phoebus |

### Proxy Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `proxy_url` | `""` | HTTP proxy URL |
| `proxy_port` | `""` | HTTP proxy port |

### NFS Mounts (Optional)

```yaml
nfsMounts:
  - name: data
    server: 192.168.197.157
    path: /data_epik8s/btf/data
    mountPath: /nfs/epik8s/data
```

### NTP Servers (Optional)

Configures time sync via `systemd-timesyncd` on Debian/Ubuntu or `chrony` on RedHat/Suse.
Leave `ntpServers` empty (the default) to skip NTP configuration entirely.

```yaml
ntpServers:
  - ntp1.lnf.infn.it
  - ntp2.lnf.infn.it
  - ntp3.lnf.infn.it
```

Example Playbook
----------------

### Using GitHub Release

```yaml
- hosts: epics_consoles
  roles:
    - role: ansible-epics-console-role
      vars:
        phoebus_version: v26.2.13b1
        # URL auto-generated from GitHub releases
        control_user: operator
        opi_main: "btf/Launcher.bob"
        opi_repos:
          - url: "https://github.com/myorg/opi-repo.git"
            dest: "btf"
            opi_main: Launcher.bob
            default: true
```

### Using Custom URL

```yaml
- hosts: epics_consoles
  roles:
    - role: ansible-epics-console-role
      vars:
        phoebus_version: v26.2.13b1
        phoebus_url: "https://github.com/infn-epics/phoebus/releases/download/v26.2.13b1/phoebus-5.0.3-SNAPSHOT-linux.tar.gz"
        control_user: operator
```

### Using Binary Server

```yaml
- hosts: epics_consoles
  roles:
    - role: ansible-epics-console-role
      vars:
        phoebus_version: 4.7.4-INFN
        # URL auto-generated from binary server
        control_user: operator
```

OPI Repository Configuration
-----------------------------

Each OPI repository can have the following fields:

```yaml
opi_repos:
  - url: "https://github.com/org/repo.git"    # Repository URL
    dest: "repo-name"                          # Destination folder
    opi_main: "Launcher.bob"                   # Main OPI file
    opi_settings: "settings_template.ini"      # Settings file (optional)
    default: true                              # Set as default OPI
    version: master                            # Git branch/tag
    opi_user: operator                         # User ownership
```

Desktop Integration
------------------

The role creates desktop shortcuts for:
- Phoebus launcher
- Phoebus navigator (file browser)

Generated in:
- `/usr/share/applications/` (system-wide)
- User's desktop (if `control_user` is specified)

Testing
-------

```bash
# Test on localhost
ansible-playbook -i localhost.yml configure-consoles.yml

# Test on remote hosts
ansible-playbook -i hosts.yml configure-consoles.yml
```

Troubleshooting
--------------

### Check downloaded version
```bash
cat /phoebus/version.txt
```

### Test download URL manually
```bash
# GitHub release
curl -I "https://github.com/infn-epics/phoebus/releases/download/v26.2.13b1/phoebus-5.0.3-SNAPSHOT-linux.tar.gz"

# Binary server
curl -I "https://opensource.lnf.infn.it/binary/epics/phoebus/linux/product-4.7.4-INFN.tar.gz"
```

### View Ansible variables
```bash
ansible-playbook playbook.yml --tags debug -vv
```

License
-------

GPL-3.0

Author Information
------------------

INFN LNF - Laboratori Nazionali di Frascati
Control System Group

