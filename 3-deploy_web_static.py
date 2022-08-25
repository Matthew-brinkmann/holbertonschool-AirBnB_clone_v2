#!/usr/bin/python3
"""
script (based on the file 1-pack_web_static.py and 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers, using the
function deploy
"""

from datetime import datetime
from os.path import exists
from pathlib import Path
from fabric.api import put, run, env, local
env.hosts = ['52.204.151.72', '3.90.36.230']
env.user = "ubuntu"
env.key_filename = ['./my_ssh_private_key']


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


def do_deploy(archive_path):
    """deploys to server"""
    if exists(archive_path) is False:
        return False
    resultOfUpload = put(archive_path, '/tmp/')
    if resultOfUpload.failed:
        return False
    deployLocation = "/data/web_static/releases/"
    archiveFileName = Path(archive_path).stem

    resultOfDirCreate = run('mkdir -p {}{}/'.format(
                            deployLocation, archiveFileName))
    if resultOfDirCreate.failed:
        print("failed to create dir: {}".format(deployLocation))
        return False

    resultOfDecompress = run('tar -C {}{} -xzf /tmp/{}.tgz'.format(
                             deployLocation, archiveFileName, archiveFileName))
    if resultOfDecompress.failed:
        print("failed to decompress: {}.tgz".format(archiveFileName))
        return False

    resultOfRemoveTmp = run('rm /tmp/{}.tgz'.format(archiveFileName))
    if resultOfRemoveTmp.failed:
        print('failed to remove temp archive')
        return False

    resultOfMoveFolderLocation = run('mv {0}{1}/web_static/* {0}{1}/'.format(
                                     deployLocation, archiveFileName))
    if resultOfMoveFolderLocation.failed:
        print('failed to move from web_static archive')
        return False

    resultOfRemoveWebStatic = run('rm -rf {}{}/web_static'.format(
                                     deployLocation, archiveFileName))
    if resultOfRemoveWebStatic.failed:
        print('failed to remove {}{}/web_static'.format(
              deployLocation, archiveFileName))
        return False

    resultofRemoveSymLink = run('rm -rf /data/web_static/current')
    if resultofRemoveSymLink.failed:
        print('failed to remove /data/web_static/current symlink')
        return False

    resultOfCreateSymLink = run('ln -s {}{}/ /data/web_static/current'.format(
                                deployLocation, archiveFileName))
    if resultOfCreateSymLink.failed:
        print('failed to create New Symlink')
        return False

    print("{} successfully deployed".format(archiveFileName))
    return True


def deploy():
    """combines pack and deploy"""
    archive_path = do_pack()
    if archive_path is None:
        print("archive failed to create")
        return False
    return do_deploy(archive_path)
