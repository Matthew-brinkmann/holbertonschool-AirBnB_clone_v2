#!/usr/bin/python3
"""
script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives,
using the function do_clean:
"""
import os
from fabric.api import *
env.hosts = ['52.204.151.72', '3.90.36.230']
env.user = "ubuntu"
env.key_filename = ['./my_ssh_private_key']


def do_clean(number=0):
    """cleans up relases folders """

    if int(number) == 0:
        number = 1
    else:
        number = int(number)

    localFiles = sorted(os.listdir("versions"))
    for i in range(number):
        localFiles.pop()
    with lcd("versions"):
        for file in localFiles:
            local("rm ./{}".format(file))

    with cd("/data/web_static/releases"):
        serverFiles = run("ls -tr").split()
        for i in range(number):
            serverFiles.pop()
        for file in serverFiles:
            run("rm -rf ./{}".format(file))
