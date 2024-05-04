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
    if number == 0:
        number = 1
    else:
        number = int(number)

    L_no_line = local(f"ls -c versions/web_static_* | wc -l")
    L_paths = local(f"ls -c versions/web_static_* | tail -n \
        {int(L_no_line) - number}").split('\n')

    for L_path in L_paths:
        local(f"sudo rm -fr {path}")

    R_no_line = run("ls -c /data/web_static/releases/web_static_* | wc -l")
    R_paths = run(f"ls -c /data/web_static/releases/web_static_* | tail -n \
        {int(R_no_line) - number}").split('\n')

    for R_path in R_paths:
        run(f"sudo rm -fr {R_path}")
