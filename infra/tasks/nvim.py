from pyinfra.api.deploy import deploy
from pyinfra.context import host
from pyinfra.facts.files import File
from pyinfra.facts.server import Arch, Home
from pyinfra.operations import files, git, server

from infra import const


@deploy("Install NeoVim")
def install_nvim():
    arch = host.get_fact(Arch)
    url = format_nvim_version(arch)
    tmp_dest = "/tmp/nvim.tgz"
    final_dest = "/usr/local"

    if not host.get_fact(File, path=f"{final_dest}/bin/nvim"):
        files.download(src=url, dest=tmp_dest, mode="0644")
        server.shell(
            f"tar zxf {tmp_dest} --strip-components 1 -C {final_dest}", _sudo=True
        )


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
        src=const.NVIM_CONF_SRC,
        user=user,
        group=user,
        dest=path,
        _sudo=True,
        _sudo_user=user,
    )

    home = host.get_fact(Home)

    files.line(line="alias vim=nvim", path=f"{home}/.zshrc", _sudo=True)


def format_nvim_version(arch: str) -> str:
    pkg_fname = "nvim-linux-"
    if arch == "amd64":
        pkg_fname += "x64_64.tar.gz"
    elif arch == "aarch64":
        pkg_fname += "arm64.tar.gz"
    else:
        raise ValueError(f"unsupported arch: {arch}")

    return f"{const.NVIM_BASE_URL}/{const.NVIM_VERSION}/{pkg_fname}"
