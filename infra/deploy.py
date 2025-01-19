from pathlib import Path

from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.operations import python, server

from . import const
from .tasks.nvim import configure_nvim
from .tasks.omz import ensure_omz
from .tasks.pkg import install_base_pkgs
from .tasks.pyenv import ensure_pyenv
from .tasks.user import configure_user


@deploy("Set up the dev lab")
def setup():
    users = host.data.get("users")
    if not users:
        raise ValueError("`users` list is missing from inventory!")

    install_base_pkgs()

    new_group = const.GROUP
    server.group(group=new_group, _sudo=True)
    server.group(group="sudo", _sudo=True)
    server.shell(
        "echo '%sudo ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo",
        name="Enable passwordless sudo",
        _sudo=True,
    )

    for user_conf in users:
        user = user_conf.get("name")
        if not user:
            logger.error("Detected a user without `name` field specified")
            continue

        home = f"/home/{user}"
        nvim_path = str(Path(home, const.NVIM_DIR))

        configure_user(user_conf)

        python.call(name="Ensure Oh My ZSH", function=ensure_omz, user=user, home=home)

        configure_nvim(user, nvim_path)

    python.call(name="Ensure pyenv", function=ensure_pyenv)
