#!/usr/bin/python3
from fabric.api import local
from time import strftime


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
