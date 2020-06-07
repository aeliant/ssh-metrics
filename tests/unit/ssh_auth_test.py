"""@package tests.unit.ssh_auth_test

All unit tests related to the model SSH Auth."""
import pytest

from mock import patch
from ssh_metrics.models import SSHAuth


@pytest.mark.unit
@patch('ssh_metrics.models.Popen')
def failed_passwords_test(mocked_popen):
    """With given input with failed passwords, check that parsing is working as expected."""
    mocked_popen.return_value.communicate.return_value = ('GeoIP Country Edition: US, United States'.encode(), None)
    # fake input
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
def failed_passwords_report_csv_test(mocked_popen):
    """Check output format is correct for csv."""
    time = '00:00:14'
    message = 'Failed password for invalid user darth.vader from 1.2.3.4 port 48302 ssh2'
    mocked_popen.return_value.communicate.return_value = ('GeoIP Country Edition: US, United States'.encode(), None)

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


