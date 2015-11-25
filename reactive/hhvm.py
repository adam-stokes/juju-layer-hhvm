import sys
from charms.reactive import (
    hook,
    when,
    set_state,
    remove_state
)

from charmhelpers.core import hookenv, host
from charmhelpers.fetch import (
    apt_update,
    apt_install,
    add_source
)

from shell import shell

config = hookenv.config()
lsb = host.lsb_release()


@hook('install')
def install_hhvm():
    """ Installs HHVM

    Emits:
    hhvm.available: Emitted once the runtime has been installed
    """
    remove_state('hhvm.available')
    hookenv.status_set('maintenance', 'Installing HHVM')

    add_source('deb http://dl.hhvm.com/ubuntu '
               '{} main'.format(lsb['DISTRIB_CODENAME']),
               key='0x5a16e7281be7a449')
    apt_update()
    apt_install(['hhvm'])

    hookenv.status_set('maintenance', 'Installing HHVM completed.')

    hookenv.status_set('active', 'ready!')
    set_state('hhvm.available')


@when('nginx.available', 'hhvm.available')
def configure_hhvm_nginx():
    sh = shell('sh /usr/share/hhvm/install_fastcgi.sh')
    if sh.code > 0:
        hookenv.status_set('blocked', 'Failed to configure HHVM for NGINX')
        sys.exit(0)
