from pyinfra.api.deploy import deploy
from pyinfra.operations import files, server

from infra import const


@deploy("Configure user & group")
def configure_user(conf: dict):
    user = conf.get("name")
    new_group = const.GROUP
    home = f"/home/{user}"

    server.user(
        user=user,
        groups=["sudo", "users", new_group],
        home=home,
        ensure_home=True,
        create_home=True,
        _sudo=True,
    )

    ssh_pub_key = conf.get("ssh_public_key")
    if ssh_pub_key:
        server.files.directory(
            name="Ensure .ssh dir",
            path=f"{home}/.ssh",
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
