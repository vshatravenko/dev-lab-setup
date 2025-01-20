GROUP = "dev"
APT_BASE_PKGS = [
    "neovim",
    "build-essential",
    "git",
    "fzf",
    "ripgrep",
    "golang",
    "npm",
    "unzip",
    "python3-venv",
]

APT_PYENV_PKGS = [
    "acl",
    "build-essential",
    "libssl-dev",
    "zlib1g-dev",
    "libbz2-dev",
    "libreadline-dev",
    "libsqlite3-dev",
    "curl",
    "git",
    "libncursesw5-dev",
    "xz-utils",
    "tk-dev",
    "libxml2-dev",
    "libxmlsec1-dev",
    "libffi-dev",
    "liblzma-dev",
]

YUM_BASE_PKGS = [
    "acl",
    "neovim",
    "git",
    "make",
    "automake",
    "fzf",
    "ripgrep",
    "golang",
    "npm",
    "unzip",
    "python3",
]

YUM_PYENV_PKGS = [
    "gcc",
    "make",
    "patch",
    "zlib-devel",
    "bzip2",
    "bzip2-devel",
    "readline-devel",
    "sqlite",
    "sqlite-devel",
    "openssl-devel",
    "tk-devel",
    "libffi-devel",
    "xz-devel",
]

PACMAN_BASE_PKGS = [
    "git",
    "curl",
    "wget",
    "neovim",
    "fzf",
    "ripgrep",
    "go",
    "npm",
    "unzip",
    "gcc",
]

PACMAN_PYENV_PKGS = ["base-devel", "openssl", "zlib", "xz", "tk", "make", "pkg-config"]


DEFAULT_PYTHON_VERSION = "3.12"

NVIM_SRC = "https://github.com/vshatravenko/nvim-conf"
NVIM_DIR = ".config/nvim"
