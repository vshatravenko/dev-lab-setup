#!/usr/bin/env python

from subprocess import run
from sys import argv

VMS = {
    "ubuntu-lab": {
        "arch": "arm64",
        "distro": "ubuntu",
        "cloud_init_path": "config/cloud-init-data.yml",
    },
    "fedora-lab": {
        "arch": "arm64",
        "distro": "fedora",
    },
}

DEFAULTS = {
    "action": "create",
    "arch": "arm64",
    "cloud_init_path": "config/cloud-init-data.yml",
}


def create_orb_vm(name: str, data: dict):
    arch = data.get("arch", DEFAULTS["arch"])
    ci_path = data.get("cloud_init_path", DEFAULTS["cloud_init_path"])
    distro = data.get("distro")

    if not distro:
        raise ValueError("`distro` field is required")

    args = ["orbctl", "create", "-a", arch, "-c", ci_path, distro, name]
    run(args)


def delete_orb_vm(name: str):
    args = ["orbctl", "delete", "-f", name]
    run(args)


if __name__ == "__main__":
    action = DEFAULTS["action"]
    if len(argv) > 1:
        action = argv[1]

    if action == "create":
        for name, data in VMS.items():
            print(f"Creating {name}")
            create_orb_vm(name, data)
    elif action == "delete":
        for name in VMS:
            print(f"Deleting {name}")
            delete_orb_vm(name)
    else:
        print(
            f"Unsupported action `{action}`, only `create` and `delete` are supported"
        )
