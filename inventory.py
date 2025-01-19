users = [
    {
        "name": "d33p",
        "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHABNMcOBuZqwHc9VF18aAeCQw3AFFGL8G4BJ/24t1Y3 vshatravenko@gmail.com",
    },
    {"name": "dark"},
    {"name": "fantasy"},
]

my_hosts = [
    #   (
    #       "@ssh/ubuntu-lab.orb.local",
    #       {"ssh_user": "ubuntu-lab", "ssh_port": 32222, "users": users},
    #   ),
    (
        "@ssh/arch-lab.orb.local",
        {"ssh_user": "arch-lab", "ssh_port": 32222, "users": users},
    ),
    #   (
    #       "@ssh/fedora-lab.orb.local",
    #       {
    #           "ssh_user": "fedora-lab",
    #           "ssh_port": 32222,
    #           "users": users
    #       },
    #   ),
    #   (
    #       "@local",
    #       {"ssh_user": "arch-lab", "ssh_port": 32222, "users": users},
    #   ),
]
