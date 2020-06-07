"""@package tests.unit.ssh_auth_test

All unit tests related to the model SSH Auth."""
import pytest

from mock import patch
from ssh_metrics.models import SSHAuth


@pytest.mark.unit
@patch('ssh_metrics.models.Popen')
def failed_passwords_test(mocked_popen):
    """With given input with failed passwords, check that parsing is working as expected."""
    # fake input
    mocked_popen.return_value.communicate.return_value = (
        'GeoIP Country Edition: US, United States'.encode(),
        None
    )
    time = '00:00:14'
    message = 'Failed password for invalid user darth.vader from 1.2.3.4 port 48302 ssh2'

    # init object and add log
    obj = SSHAuth(hostname='coruscant', day='May 14')
    obj.add_log(time, message)

    # checking failed passwords
    failed = obj.failed_passwords()
    assert len(failed) == 1
    assert {'time', 'user', 'src_ip', 'src_geoip'} == set(failed[0].keys())
    assert '00:00:14' == failed[0].get('time')
    assert 'darth.vader' == failed[0].get('user')
    assert '1.2.3.4' == failed[0].get('src_ip')
    assert 'US' in failed[0].get('src_geoip')

    # checking failed passwords with country stats only
    failed = obj.failed_passwords(country_stats=True)
    assert isinstance(failed, dict)
    assert {'US, United States': 1} == failed


@pytest.mark.unit
@patch('ssh_metrics.models.Popen')
def invalid_users_test(mocked_popen):
    """With given input of invalid users, check that parsing is working as expected."""
    mocked_popen.return_value.communicate.return_value = (
        'GeoIP Country Edition: US, United States'.encode(),
        None
    )
    time = '00:00:14'
    message = 'Invalid user darth.vader from 1.2.3.4 port 48302'

    # init object and add log
    obj = SSHAuth(hostname='kashyyk', day='May 14')
    obj.add_log(time, message)

    # checking invalid user
    failed = obj.invalid_users()
    assert len(failed) == 1
    assert {'time', 'user', 'src_ip', 'src_geoip'} == set(failed[0].keys())
    assert '00:00:14' == failed[0].get('time')
    assert 'darth.vader' == failed[0].get('user')
    assert '1.2.3.4' == failed[0].get('src_ip')
    assert 'US' in failed[0].get('src_geoip')

    # checking invalid users with country stats only
    failed = obj.invalid_users(country_stats=True)
    assert isinstance(failed, dict)
    assert {'US, United States': 1} == failed


@pytest.mark.unit
@patch('ssh_metrics.models.Popen')
def accepted_connections_test(mocked_popen):
    """With given input of accepted connections, check that parsing is working as exepcted."""
    mocked_popen.return_value.communicate.return_value = (
        'GeoIP Country Edition: US, United States'.encode(),
        None
    )
    time = '00:00:14'
    message = 'Accepted publickey for darth.vader from 1.2.3.4 port 4444 ssh2: RSA SHA256:xxxxxxxx'
    time2 = '00:00:15'
    message2 = 'Accepted password for luke.skywalker from 1.2.3.5 port 4444 ssh2'

    # init object and add log
    obj = SSHAuth(hostname='kashyyk', day='May 14')
    obj.add_log(time, message)
    obj.add_log(time2, message2)

    # checking accepted connections
    failed = obj.accepted_connections()
    assert {'time', 'user', 'auth', 'src_ip', 'src_geoip'} == set(failed[0].keys())
    assert {'00:00:14', '00:00:15'} == set([_.get('time') for _ in failed])
    assert {'darth.vader', 'luke.skywalker'} == set([_.get('user') for _ in failed])
    assert {'publickey', 'password'} == set([_.get('auth') for _ in failed])
    assert {'1.2.3.4', '1.2.3.5'} == set([_.get('src_ip') for _ in failed])

    if failed[0].get('user') == 'darth.vader':
        assert 'publickey' == failed[0].get('auth')
        assert 'password' == failed[1].get('auth')
    else:
        assert 'publickey' == failed[1].get('auth')
        assert 'password' == failed[0].get('auth')


@pytest.mark.unit
@patch('ssh_metrics.models.Popen')
def failed_passwords_report_csv_test(mocked_popen):
    """Check output format is correct for csv."""
    time = '00:00:14'
    message = 'Failed password for invalid user darth.vader from 1.2.3.4 port 48302 ssh2'
    mocked_popen.return_value.communicate.return_value = (
        'GeoIP Country Edition: US, United States'.encode(),
        None
    )

    # init object and add log
    obj = SSHAuth(hostname='coruscant', day='May 14')
    obj.add_log(time, message)

    # checking normal report
    report = obj.report(SSHAuth.FAILED_PASSWORDS, format='csv')
    assert isinstance(report, str), report
    report = report.split('\n')
    assert {'Time', 'User', 'Src ip', 'Src geoip'} == set(report[0].split(';'))
    assert {'00:00:14', 'darth.vader', '1.2.3.4', 'US, United States'} == set(report[1].split(';'))

    # checking with country stats
    report = obj.report(SSHAuth.FAILED_PASSWORDS, format='csv', country_stats=True)
    assert isinstance(report, str)
    report = report.split('\n')
    assert {'GeoIP', 'Count'} == set(report[0].split(';'))
    assert {'US, United States', '1'} == set(report[1].split(';'))
