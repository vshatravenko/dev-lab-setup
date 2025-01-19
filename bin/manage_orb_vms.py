#!/usr/bin/env python

import argparse
from subprocess import run

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
    "arch-lab": {
        "arch": "arm64",
        "distro": "arch",
        "cloud_init_enabled": False,
    },
}

DEFAULTS = {
    "action": "create",
    "arch": "arm64",
    "cloud_init_path": "config/cloud-init-data.yml",
    "cloud_init_enabled": True,
}

ACTIONS = ["create", "delete"]


def create_orb_vm(name: str, data: dict):
    arch = data.get("arch", DEFAULTS["arch"])
    ci_enabled = data.get("cloud_init_enabled", DEFAULTS["cloud_init_enabled"])
    ci_path = data.get("cloud_init_path", DEFAULTS["cloud_init_path"])
    distro = data.get("distro")

    if not distro:
        raise ValueError("`distro` field is required")

    args = ["orbctl", "create", "-a", arch, distro, name]

    if ci_enabled:
        args.extend(["-c", ci_path])

    run(args)


def delete_orb_vm(name: str):
    args = ["orbctl", "delete", "-f", name]
    run(args)


def handle(action: str, names: list[str]):
    machines = {}
    if not names:
        machines = VMS
    else:
        machines = dict((k, dict(VMS[k])) for k in VMS if k in names)

    if not machines:
        print(f"No VM definitions found for {names}!")
        return

    print(f"Will {action} {machines.keys()}")

    if action == "create":
        for name, data in machines.items():
            print(f"Creating {name}")
            create_orb_vm(name, data)
    elif action == "delete":
        for name in machines:
            print(f"Deleting {name}")
            delete_orb_vm(name)
    else:
        print(
            f"Unsupported action `{action}`, only `create` and `delete` are supported"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage OrbStack VMs (macOS-only)")
    parser.add_argument(
        "--action",
        "-a",
        type=str,
        default=DEFAULTS["action"],
        choices=ACTIONS,
        help="action to use",
    )

    parser.add_argument(
        "--names",
        "-n",
        type=str,
        help="name of the VM to use",
    )

    args = parser.parse_args()

    handle(args.action, args.names.split(","))
