from pyinfra.operations.server import files

SYSTEM_ENV_FILE = "/etc/environment"


def set_proxy_vars(proxies: dict):
    for var, proxy in proxies.items():
        files.line(path=SYSTEM_ENV_FILE, line=f"export {var}={proxy}", _sudo=True)
