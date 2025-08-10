# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "packaging"
# ]
# ///
import os
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
    subprocess.run(["git", "fetch", "origin", "gh-pages:gh-pages"], check=True)
    v = packaging.version.parse(version(os.environ["PACKAGE_NAME"]))
    latest = get_latest()
    cmd = ["mike", "deploy", "--push", "--update-aliases", f"{v.major}.{v.minor}"]
    if v.is_prerelease:
        cmd.append("prerelease")
    elif latest is None or (v.major, v.minor) > latest:
        cmd.append("latest")
    print(f"Running {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    subprocess.run(["mike", "set-default", "--push", "latest"], check=True)


if __name__ == "__main__":
    deploy()
