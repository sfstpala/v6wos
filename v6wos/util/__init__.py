import uuid
import os
import shlex
import subprocess
import functools


def b32encode(n):
    charset = "0123456789abcdefghjkmnpqrstvwxyz"
    s = []
    while n > 0:
        r = n % 32
        n //= 32
        s.append(charset[r])
    if len(s) > 0:
        s.reverse()
    else:
        s.append('0')
    return ''.join(s)


def random_id():
    return b32encode(int.from_bytes(
        uuid.uuid4().bytes, "big")).ljust(26, "0")


@functools.lru_cache()
def get_git_revision():
    git_dir = os.path.join(os.path.dirname(os.path.realpath(
        os.path.join(__file__, "..", ".."))), ".git")
    status, output = subprocess.getstatusoutput(
        "git --git-dir={} rev-parse --short HEAD".format(
            shlex.quote(git_dir)))
    return output.strip() if status == 0 else None
