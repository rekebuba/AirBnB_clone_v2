#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
"""
from fabric.api import *
import os

env.hosts = ['54.175.224.158', '100.25.129.156']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def deploy():
    """
    A Fabric script that creates and distributes an archive to web servers,
    using the function deploy
    """
    archive_path = do_pack()
    if not os.path.exists(archive_path):
        return False

    return do_deploy(archive_path)
