#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
"""
from fabric.api import *
from time import strftime
import os
import re


env.hosts = ['54.175.224.158', '100.25.129.156']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    A Fabric script that generates a .tgz archive
    from the contents of the web_static folder
    """
    file_name = strftime('%Y%m%d%H%M%S')
    try:
        local('mkdir -p versions')
        local(f'tar -czvf versions/web_static_{file_name}.tgz web_static')

        return f"versions/web_static_{file_name}.tgz"
    except Exception as e:
        return None


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
        run(f"sudo mkdir -p /data/web_static/releases/{file_name}/")
        run(f"sudo tar -xzf /tmp/{file_name}.tgz \
-C /data/web_static/releases/{file_name}/")
        run(f"sudo rm /tmp/{file_name}.tgz")
        run(f'sudo mv /data/web_static/releases/{file_name}/web_static/* \
/data/web_static/releases/{file_name}/')
        run(f'sudo rm -rf /data/web_static/releases/\
{file_name}/web_static')
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s /data/web_static/releases/{file_name}/ \
/data/web_static/current")
    except Exception:
        return False

    return True


def deploy():
    """
    A Fabric script that creates and distributes an archive to web servers,
    using the function deploy
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
