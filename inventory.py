my_hosts = [
    (
        "@ssh/ubuntu-lab.orb.local",
        {
            "ssh_user": "ubuntu-lab",
            "ssh_port": 32222,
            "users": [
                {
                    "name": "d33p",
                    "ssh_public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHABNMcOBuZqwHc9VF18aAeCQw3AFFGL8G4BJ/24t1Y3 vshatravenko@gmail.com",
                },
                {"name": "dark"},
                {"name": "fantasy"},
            ],
        },
    ),
    #   (
    #       "@ssh/fedora-lab.orb.local",
    #       {
    #           "ssh_user": "fedora-lab",
    #           "ssh_port": 32222,
    #           "users": ["d33p", "dark", "fantasy"],
    #       },
    #   ),
]
