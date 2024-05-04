#!/usr/bin/python3
from fabric.api import local

def do_pack():
    result = local('uname -s', capture=True)
    print(result.stdout)
