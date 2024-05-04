#!/usr/bin/python3

from fabric.api import local
from datetime import datetime

def do_pack():
    result = local('ls -l', capture=True)
    print(result.stdout)
