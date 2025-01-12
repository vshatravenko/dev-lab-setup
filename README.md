# Dev Lab Setup Automation

This repository contains `pyinfra`-powered dev lab setup automation

## Prerequisites

* Supported Linux target host(Ubuntu/Debian/Fedora/CentOS)
* `pyinfra` installed

```sh
    pip install pyinfra
```

## Usage

This repository contains automation to set up a ready-to-use dev lab environment for Ubuntu/Debian hosts.
To initiate the setup:

1. Set target host details in `inventory.py`
2. Run `pyinfra -y inventory.py main.py`, add `--debug` flag to get more execution details

Once this is done, specified users will be available on target hosts with NeoVim and Oh my ZSH installed

## Development

If you'd like to quickly spin up target hosts utilizing different Linux distros,
run `bin/manage_orb_vms.py`

To clean up the testing environment, run `bin/manage_orb_vms.py delete`
