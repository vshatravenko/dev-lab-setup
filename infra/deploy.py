from pathlib import Path

from pyinfra import logger
from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.operations import files, git, python, server

from . import const
from .tasks.omz import ensure_omz
from .tasks.pkg import install_base_pkgs
from .tasks.pyenv import ensure_pyenv


@deploy("Set up the dev lab")
def setup():
    users = host.data.get("users")
    if not users:
        raise ValueError("`users` list is missing from inventory!")

    install_base_pkgs()

    for user_conf in users:
        user = user_conf.get("name")
        if not user:
            logger.error("Detected a user without `name` field specified")
            continue

        new_group = const.GROUP
        server.group(group="sudo", _sudo=True)
        server.shell(
            "echo '%sudo ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo",
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

        ssh_pub_key = user_conf.get("ssh_public_key")
        if ssh_pub_key:
            server.files.directory(
                name="Ensure .ssh dir",
                path=f"home/.ssh",
                user=user,
                group=user,
                recursive=True,
                _sudo=True,
                _sudo_user=user,
            )

            files.line(
                name="Authorize SSH pub key",
                path=f"{home}/.ssh/authorized_keys",
                line=ssh_pub_key,
                _sudo=True,
                _sudo_user=user,
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

        python.call(name="Ensure Oh My ZSH", function=ensure_omz, user=user, home=home)

    python.call(name="Ensure pyenv", function=ensure_pyenv)
