#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py)
"""
from fabric.api import *


env.hosts = ['54.175.224.158', '100.25.129.156']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """
    A Fabric script that deletes out-of-date archives,
    using the function do_clean:
    """
    number = 1 if int(number) == 0 else int(number)

    L_no_line = int(local(f"ls versions/ | grep 'web_static_' | wc -l",
                          capture=True))
    if L_no_line < number:
        L_no_line = number
    L_paths = local(f"ls -t versions/ | grep 'web_static_' | tail -n \
        {L_no_line - number}", capture=True).split()

    for L_path in L_paths:
        if L_path != '':
            local(f"sudo rm -fr versions/{L_path}")

    R_no_line = int(run("ls /data/web_static/releases/ | grep 'web_static_' \
| wc -l"))
    if R_no_line < number:
        R_no_line = number
    R_paths = run(f"ls -t /data/web_static/releases/ | grep 'web_static_' \
| tail -n {R_no_line - number}").split()

    for R_path in R_paths:
        if R_path != '':
            run(f"sudo rm -fr /data/web_static/releases/{R_path}")
