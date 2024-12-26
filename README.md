# Dev Lab Setup Automation

## Prerequisites

```sh
    pip install pyinfra
```

## Usage

This repository contains automation to set up a ready-to-use dev lab environment for Ubuntu/Debian hosts.
To initiate the setup:

1. Set target host details in `inventory.py`
2. Run `pyinfra -y inventory.py main.py`, add `--debug` flag to get more execution details

Once this is done, `dev` user will be available at the target host, ready to be used!
