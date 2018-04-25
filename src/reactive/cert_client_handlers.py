from charms.reactive import (
    hook,
    is_state,
    remove_state,
    set_state,
    when,
    when_not,
)

from charmhelpers.fetch.ubuntu import (
    apt_install
)
from charmhelpers.core import hookenv

@when_not('installed')
def install():
    apt_install(['apache2'])
    set_state('installed')
    hookenv.status_set('active', 'Ready')

@when('certificates.available')
def request_vert(tls):
    common_name = hookenv.unit_public_ip()
    sans = set()
    sans.add(hookenv.unit_public_ip())
    sans = list(sans)
    certificate_name = hookenv.local_unit().replace('/', '_')
    tls.request_server_cert(common_name, sans, certificate_name)
    tls.add_request_server_cert(common_name, sans, certificate_name)
    tls.add_request_server_cert('admin.keystone.openstack.local', [], 'admin_keystone')
    tls.add_request_server_cert('internal.keystone.openstack.local', [], 'internal_keystone')
    tls.add_request_server_cert('public.keystone.openstack.local', [], 'public_keystone')
    tls.request_server_certs()

