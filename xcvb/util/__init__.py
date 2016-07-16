import base64
import uuid
import os
import shlex
import subprocess
import functools


def random_id(seed=None, length=22):
    seed = seed or uuid.uuid4().bytes
    return base64.urlsafe_b64encode(seed).decode().rstrip("=")[:length]


@functools.lru_cache()
def get_git_revision():
    git_dir = os.path.join(os.path.dirname(os.path.realpath(
        os.path.join(__file__, "..", ".."))), ".git")
    status, output = subprocess.getstatusoutput(
        "git --git-dir={} rev-parse --short HEAD".format(
            shlex.quote(git_dir)))
    return output.strip() if status == 0 else None
