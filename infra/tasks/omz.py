from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.server import Home, LinuxName
from pyinfra.operations import apt, files, python, server

from .. import const

OMZ_SRC = "https://install.ohmyz.sh/"


@deploy("Install Oh My ZSH")
def install_omz(user: str, home: str):
    server.packages("zsh", _sudo=True)

    python.call(name="Set default shell to ZSH", function=configure_shell, user=user)

    files.directory(
        name="Remove existing Oh My ZSH files",
        path=f"{home}/.oh-my-zsh",
        present=False,
        _sudo_user=user,
        _sudo=True,
    )

    omz_dest = f"{home}/omz-install.sh"
    files.download(
        name="Download OMZ installation script",
        src=OMZ_SRC,
        dest=omz_dest,
        user=user,
        group=user,
        _sudo_user=user,
        _sudo=True,
    )

    server.shell(
        name="Install Oh My ZSH",
        commands=[f"sh {omz_dest}"],
        _chdir=home,
        _env={"USER": user, "HOME": home},
        _sudo_user=user,
        _sudo=True,
    )

    files.file(
        name="Clean up OMZ installation script",
        path=omz_dest,
        present=False,
        _sudo=True,
    )


def configure_shell(user: str):
    ok, out = host.run_shell_command(f"grep {user}:x /etc/passwd")
    if not ok:
        raise Exception(f"Could not determine the user's shell: {out.stderr}")

    current = out.stdout
    if "zsh" not in current:
        server.shell(
            name="Change shell to ZSH",
            commands=[f"chsh --shell $(which zsh) {user}"],
            _sudo=True,
        )
    else:
        host.noop("Shell already set to ZSH, skipping")
