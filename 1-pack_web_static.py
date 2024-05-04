#!/usr/bin/python3
from fabric.api import local

def do_pack():
    local('uname -s')
    print(result.stdout)
