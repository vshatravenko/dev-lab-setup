from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.server import LinuxName
from pyinfra.operations import apt, pacman, server, yum

from infra import const

SUPPORTED_DISTROS = (
    "Debian",
    "Ubuntu",
    "Fedora",
    "CentOS",
    "Arch Linux",
    "Arch Linux ARM",
    "Manjaro",
    "Manjaro ARM",
)


@deploy("Install base packages")
def install_base_pkgs():
    os_name = host.get_fact(LinuxName)
    logger.info(f"Processing OS: {os_name}")

    if os_name not in SUPPORTED_DISTROS:
        raise Exception(
            f"Detected unsupported OS distribution: {os_name}, only {SUPPORTED_DISTROS} are supported"
        )

    update_pkg_list()

    if os_name in ["Debian", "Ubuntu"]:
        server.packages(packages=const.APT_BASE_PKGS, _sudo=True)
    elif os_name in ["Fedora", "CentOS"]:
        server.packages(packages=const.YUM_BASE_PKGS, _sudo=True)
    elif os_name in ["ArchLinux", "Arch Linux ARM", "Manjaro", "Manjaro ARM"]:
        server.packages(packages=const.PACMAN_BASE_PKGS, _sudo=True)


def install_pkg_factory():
    os_name = host.get_fact(LinuxName)

    def install_pkg(pkgs: list[str]):
        if os_name not in SUPPORTED_DISTROS:
            raise Exception(
                f"Detected unsupported OS distribution: {os_name}, only {SUPPORTED_DISTROS} are supported"
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
