"""@package tests.unit.ssh_auth_test

All unit tests related to the model SSH Auth."""
import pytest

from ssh_metrics.models import SSHAuth


@pytest.mark.unit
def failed_passwords_test():
    """With given input with failed passwords, check that parsing is working as expected."""
    # fake input
    time = '00:00:14'
    message = 'Failed password for invalid user darth.vader from 1.2.3.4 port 48302 ssh2'

    # init object and add log
    obj = SSHAuth(hostname='coruscant', day='May 14')
    obj.add_log(time, message)

    # checking failed passwords
    failed = obj.failed_passwords
    assert len(failed) == 1
    assert {'time', 'user', 'src_ip', 'src_geoip'} == set(failed[0].keys())
    assert '00:00:14' == failed[0].get('time')
    assert 'darth.vader' == failed[0].get('user')
    assert '1.2.3.4' == failed[0].get('src_ip')
    assert 'US' in failed[0].get('src_geoip')

    