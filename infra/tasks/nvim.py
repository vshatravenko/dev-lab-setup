from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.server import Home
from pyinfra.operations import files, git, server

from infra import const


@deploy("Configure NeoVim")
def configure_nvim(user: str, path: str):
    server.files.directory(
        path=path,
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
        dest=path,
        _sudo=True,
        _sudo_user=user,
    )

    home = host.get_fact(Home)

    files.line(line="alias vim=nvim", path=f"{home}/.zshrc", _sudo=True)
