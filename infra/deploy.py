from pyinfra.api.deploy import deploy
from pyinfra.operations import apt, git, server

from . import const
from .tasks.omz import install_omz


@deploy("Set up the dev lab")
def setup():
    server.group(group="sudo", _sudo=True)
    server.user(
        user=const.USER,
        groups=["sudo", "users", "dev"],
        ensure_home=True,
        create_home=True,
        _sudo=True,
    )

    apt.update(_sudo=True, _sudo_user="root")
    apt.packages(
        name="Ensure NeoVim package is installed",
        packages=const.PACKAGES,
        latest=True,
        _sudo=True,
    )

    server.files.directory(
        path=const.NVIM_DEST,
        user=const.USER,
        group=const.USER,
        recursive=True,
        _sudo=True,
        _sudo_user=const.USER,
    )
    git.repo(
        src=const.NVIM_SRC,
        user=const.USER,
        group=const.USER,
        dest=const.NVIM_DEST,
        _sudo=True,
        _sudo_user=const.USER,
    )

    install_omz()
