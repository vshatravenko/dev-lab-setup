USER = "dev"
GROUP = "users"
HOME_PATH = f"/home/{USER}"
PACKAGES = [
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

NVIM_SRC = "https://github.com/vshatravenko/nvim-conf"
NVIM_DEST = f"{HOME_PATH}/.config/nvim"
