from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.server import LinuxName
from pyinfra.operations import apt, files, python, server

from .. import const

OMZ_SRC = "https://install.ohmyz.sh/"
OMZ_DEST = f"{const.HOME_PATH}/omz-install.sh"

os_name = host.get_fact(LinuxName)


@deploy("Install Oh My ZSH")
def install_omz():
    if os_name in ["Debian", "Ubuntu"]:
        apt.packages(name="Install ZSH", packages=["zsh"], _sudo=True)
    else:
        raise Exception(
            f"Detected unsupported OS distribution: {os_name}, only Debian and Ubuntu are supported"
        )

    python.call(name="Set default shell to ZSH", function=configure_shell)

    files.directory(
        name="Remove existing Oh My ZSH files",
        path=f"{const.HOME_PATH}/.oh-my-zsh",
        present=False,
        _sudo_user=const.USER,
        _sudo=True,
    )

    files.download(
        name="Download OMZ installation script",
        src=OMZ_SRC,
        dest=OMZ_DEST,
        user=const.USER,
        group=const.USER,
        _sudo_user=const.USER,
        _sudo=True,
    )

    server.shell(
        name="Install Oh My ZSH",
        commands=[f"sh {OMZ_DEST}"],
        _chdir=const.HOME_PATH,
        _env={"USER": const.USER, "HOME": const.HOME_PATH},
        _sudo_user=const.USER,
        _sudo=True,
    )

    files.file(
        name="Clean up OMZ installation script",
        path=OMZ_DEST,
        present=False,
        _sudo=True,
    )


def configure_shell():
    ok, out = host.run_shell_command(f"grep {const.USER}:x /etc/passwd")
    if not ok:
        raise Exception(f"Could not determine the user's shell: {out.stderr}")

    current = out.stdout
    if "zsh" not in current:
        server.shell(
            name="Change shell to ZSH",
            commands=[f"chsh --shell $(which zsh) {const.USER}"],
            _sudo=True,
        )
    else:
        host.noop("Shell already set to ZSH, skipping")
