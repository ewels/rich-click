# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "packaging"
# ]
# ///
from importlib.metadata import version
import subprocess
import json

import packaging.version


def get_latest():
    res = subprocess.run(["mike", "list", "latest", "-j"], stdout=subprocess.PIPE)
    if not res.stdout:  # First deploy
        return None
    data = json.loads(res.stdout)
    major, minor, *_ = data["version"].split(".")
    return int(major), int(minor)


def deploy():
    v = packaging.version.parse(version("rich-click"))
    latest = get_latest()
    cmd = ["mike", "deploy", "--update-aliases", f"{v.major}.{v.minor}"]
    if v.is_prerelease:
        cmd.append("prerelease")
    elif latest is None or (v.major, v.minor) > latest:
        cmd.append("latest")
    print(f"Running {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    subprocess.run(["git", "push", "--force", "origin", "gh-pages"], check=True)
    subprocess.run(["mike", "set-default", "--push", "latest"], check=True)


if __name__ == "__main__":
    deploy()
