#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
"""
from fabric.api import *
import os
import re


env.hosts = ['54.175.224.158', '100.25.129.156']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    A Fabric script that distributes an archive to
    web servers, using the function do_deploy
    """
    try:
        if not os.path.exists(archive_path):
            return False

        file_name = re.search(r"web_static_\d*", archive_path).group()
        put(archive_path, "/tmp/")
        run(f"sudo mkdir -p /data/web_static/releases/{file_name}")
        run(f"sudo tar -xzf /tmp/{file_name}.tgz \
-C /data/web_static/releases/{file_name}/")
        run(f"sudo rm /tmp/{file_name}.tgz")
        run(f'sudo mv /data/web_static/releases/{file_name}/web_static/* \
/data/web_static/releases/{file_name}/')
        run(f'sudo rm -rf /data/web_static/releases/\
{file_name}/web_static')
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s -f /data/web_static/releases/{file_name} \
/data/web_static/current")
    except Exception as e:
        return False

    return True
