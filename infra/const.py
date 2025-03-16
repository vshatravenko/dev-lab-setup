GROUP = "dev"
APT_BASE_PKGS = [
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
    "git",
    "make",
    "automake",
    "fzf",
    "ripgrep",
    "golang",
    "npm",
    "unzip",
    "python3",
    "glibc",
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
    "glibc",
]

PACMAN_BASE_PKGS = [
    "git",
    "curl",
    "wget",
    "fzf",
    "ripgrep",
    "go",
    "npm",
    "unzip",
    "gcc",
    "glibc",
]

PACMAN_PYENV_PKGS = ["base-devel", "openssl", "zlib", "xz", "tk", "make", "pkg-config"]


DEFAULT_PYTHON_VERSION = "3.12"

NVIM_BASE_URL = "https://github.com/neovim/neovim/releases/download"
NVIM_VERSION = "v0.10.4"

NVIM_CONF_SRC = "https://github.com/vshatravenko/nvim-conf"
NVIM_DIR = ".config/nvim"
