from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.server import Home, LinuxName
from pyinfra.operations import files, server

from infra import const

PYENV_SRC = "https://pyenv.run"
PYENV_INSTALLER_PATH = "/opt/pyenv-install.sh"
PYENV_ROOT = "/opt/pyenv"


def ensure_pyenv():
    is_installed = server.shell(
        name="Check for pyenv presence",
        commands=["zsh -c 'source $HOME/.zshrc; command -v pyenv'"],
        _sudo=True,
    )

    if is_installed.did_error():
        install_pyenv()


@deploy("Install pyenv")
def install_pyenv():
    files.download(
        name="Download pyenv installer",
        src=PYENV_SRC,
        dest=PYENV_INSTALLER_PATH,
        user="root",
        group="root",
        _sudo=True,
    )

    server.shell(
        name="Run the installer",
        commands=[f"bash {PYENV_INSTALLER_PATH}"],
        _env={"PYENV_ROOT": PYENV_ROOT},
        _sudo=True,
    )

    install_build_deps()

    server.shell(
        name="Ensure $PYENV_ROOT access",
        commands=[f"chmod -R a+rwx {PYENV_ROOT}; setfacl -Rdm m::rwx {PYENV_ROOT}"],
        _sudo=True,
    )

    py_version = host.data.get("python_version", const.DEFAULT_PYTHON_VERSION)
    server.shell(
        name=f"Install Python v{py_version}",
        commands=[f"zsh -c 'source $HOME/.zshrc; pyenv install -v {py_version}'"],
        _env={"PYENV_ROOT": PYENV_ROOT},
        _sudo=True,
    )

    server.shell(
        name="Set global Python version",
        commands=[f"zsh -c 'source $HOME/.zshrc; pyenv global {py_version}'"],
        _env={"PYENV_ROOT": PYENV_ROOT},
        _sudo=True,
    )

    users = ["root"]
    users_data = host.data.get("users", [])
    if users_data:
        users.extend([user["name"] for user in users_data])

    for user in users:
        logger.info(f"Ensuring pyenv config in .zshrc for {user}")
        update_zshrc(user)

    files.file(
        name="Clean up pyenv installer",
        path=PYENV_INSTALLER_PATH,
        present=False,
        _sudo=True,
    )


@deploy("Install build dependencies")
def install_build_deps():
    os_name = host.get_fact(LinuxName)

    pkgs = []
    if os_name in ["Ubuntu", "Debian"]:
        pkgs = const.APT_PYENV_PKGS
    elif os_name in ["Fedora", "CentOS", "RHEL"]:
        pkgs = const.YUM_PYENV_PKGS
    elif os_name in [
        "Arch Linux",
        "Arch Linux ARM",
        "Manjaro Linux",
        "Manjaro Linux ARM",
    ]:
        pkgs = const.PACMAN_PYENV_PKGS

    server.packages(name="Ensure packages", packages=pkgs, _sudo=True)


@deploy("Configure .zshrc to use pyenv")
def update_zshrc(user: str):
    lines = [
        f'export PYENV_ROOT="{PYENV_ROOT}"',
        '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"',
        'eval "$(pyenv init - zsh)"',
    ]

    home = host.get_fact(Home, user=user)

    for line in lines:
        files.line(path=f"{home}/.zshrc", line=line, _sudo=True)
