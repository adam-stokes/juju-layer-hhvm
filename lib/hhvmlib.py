import sys
import os
from shell import shell
from charmhelpers.core import hookenv


def app_path():
    """ Returns application path

    Returns:
    app_path of application location
    """
    config = hookenv.config()
    return config['app-path']


def install_composer():
    """ Installs composer
    """
    hookenv.status_set('maintenance', 'Installing composer')
    sh = shell("curl -sS https://getcomposer.org/installer | php")
    if sh.code > 0:
        hookenv.status_set(
            'blocked',
            'Unable to install composer: {}'.format(sh.errors()))
        sys.exit(0)

    sh = shell("mv composer.phar /usr/local/bin/composer")
    if sh.code > 0:
        hookenv.status_set(
            'blocked',
            'Unable to move composer to bin path: {}'.format(sh.errors()))
        sys.exit(0)
    hookenv.status_set('active', 'ready')


def composer(cmd):
    """ Runs composer

    Usage:

      composer('install')

    Arguments:
    cmd: command to run with composer

    Returns:
    Halts on error
    """
    hookenv.status_set(
        'maintenance',
        'Installing PHP dependencies in {}'.format(app_path()))
    if not os.path.isdir(app_path()):
        os.makedirs(app_path())
    os.chdir(app_path())
    if not isinstance(cmd, str):
        hookenv.status_set('blocked', '{}: should be a string'.format(cmd))
        sys.exit(0)
    cmd = ("composer {}".format(cmd))
    sh = shell(cmd)
    if sh.code > 0:
        hookenv.status_set("blocked", "Composer error: {}".format(sh.errors()))
        sys.exit(0)
    hookenv.status_set('active', 'ready')
