#!/usr/bin/python3
"""
script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives,
using the function do_clean:
"""
from fabric.api import *

env.hosts = ['52.204.151.72', '3.90.36.230']
env.user = "ubuntu"
env.key_filename = ['./my_ssh_private_key']


def do_clean(number=0):
    """cleans up relases folders """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    serverPath = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(
        serverPath, number))
