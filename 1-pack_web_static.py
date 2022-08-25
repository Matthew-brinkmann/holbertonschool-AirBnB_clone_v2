#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo,
using the function do_pack
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """generates a .tgz pack"""
    fileCreateDate = datetime.now().strftime("%Y%m%d%H%M%S")
    local('mkdir -p versions')
    newArchivePath = "versions/web_static_{}.tgz".format(fileCreateDate)
    resultOfCreate = local("tar -cvzf {} web_static".format(newArchivePath))
    if resultOfCreate.failed:
        return None
    else:
        return newArchivePath
