from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.server import LinuxName
from pyinfra.operations import apt, pacman, server, yum

from infra import const

SUPPORTED_DISTROS = ["Debian", "Ubuntu", "Fedora", "CentOS", "Arch", "Manjaro"]


@deploy("Install base packages")
def install_base_pkgs():
    os_name = host.get_fact(LinuxName)
    logger.info(f"Detected {os_name} OS name")

    if os_name in ["Debian", "Ubuntu"]:
        server.packages(packages=const.UBUNTU_PACKAGES, _sudo=True)
    elif os_name in ["Fedora", "CentOS"]:
        server.packages(packages=const.FEDORA_PACKAGES, _sudo=True)


def install_pkg_factory():
    os_name = host.get_fact(LinuxName)

    def install_pkg(pkgs: list[str]):
        if os_name not in SUPPORTED_DISTROS:
            raise Exception(
                f"Detected unsupported OS distribution: {os_name}, only Debian and Ubuntu are supported"
            )

        if os_name in ["Debian", "Ubuntu"]:
            apt.packages(packages=pkgs, name=f"Install {pkgs}", _sudo=True)
        elif os_name in ["Fedora", "CentOS"]:
            yum.packages(packages=pkgs, update=True, name=f"Install {pkgs}", _sudo=True)

    return install_pkg


def update_pkg_list():
    os_name = host.get_fact(LinuxName)

    if os_name in ["Debian", "Ubuntu"]:
        apt.update(_sudo=True, _sudo_user="root")
    elif os_name in ["Fedora", "CentOS"]:
        yum.update(_sudo=True, _sudo_user="root")
    elif os_name in ["Arch", "Manjaro"]:
        pacman.update(_sudo=True, _sudo_user="root")
