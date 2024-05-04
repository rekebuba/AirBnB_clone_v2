#!/usr/bin/python3
from fabric.api import *
import os
import re


env.hosts = ['54.175.224.158']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/authorized_keys'


def do_deploy(archive_path):
    """
    A Fabric script that distributes an archive to
    web servers, using the function do_deploy
    """
    if os.path.exists(archive_path):
        try:
            file_name = re.search(r"web_static_\d*", archive_path).group()
            put("archive_path", "/temp/")
            run(f"mkdir -p /data/web_static/releases/{file_name}")
            run(f"tar -xzf /data/web_static/releases/{file_name}.tgz \
                -C /data/web_static/releases/{file_name}")
            run(f"rm /tmp/{file_name}.tgz")
            run("rm /data/web_static/current")
            run(f"ln -s -f /data/web_static/releases/{file_name} \
                /data/web_static/current")
        except Exception:
            return False
    else:
        return False
