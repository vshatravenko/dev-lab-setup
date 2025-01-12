from pathlib import Path

from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.operations import git, server

from . import const
from .tasks.omz import install_omz
from .tasks.pkg import install_base_pkgs


@deploy("Set up the dev lab")
def setup():

    users = host.data.get("users")
    if not users:
        raise ValueError("`users` list is missing from inventory!")

    install_base_pkgs()

    for user in users:
        new_group = const.GROUP
        server.group(group="sudo", _sudo=True)
        server.shell(
            f"echo '%sudo ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo",
            name="Enable passwordless sudo",
            _sudo=True,
        )
        server.group(group=new_group, _sudo=True)

        home = f"/home/{user}"
        logger.info(f"Using home: {home}")
        server.user(
            user=user,
            groups=["sudo", "users", new_group],
            home=home,
            ensure_home=True,
            create_home=True,
            _sudo=True,
        )

        nvim_path = str(Path(home, const.NVIM_DIR))
        server.files.directory(
            path=nvim_path,
            user=user,
            group=user,
            recursive=True,
            _sudo=True,
            _sudo_user=user,
        )

        git.repo(
            src=const.NVIM_SRC,
            user=user,
            group=user,
            dest=nvim_path,
            _sudo=True,
            _sudo_user=user,
        )

        install_omz(user, home)
