"""This script retrieve metrics of SSH connections for a given day."""
import click
import json
import re
import subprocess
import sys

from datetime import datetime, timedelta

from .models import SSHAuth
from .regexes import MAIN_REGEX


__version__ = '0.0.1'
__author__ = 'Hamza ESSAYEGH'


def _write_to_output(data, output, format='txt'):
    if format == 'txt' or format == 'csv':
        with open(output, 'w') as _f:
            _f.write(data)
            _f.write('\n')
    elif format == 'json':
        json.dump(data, open(output, 'w'), indent=4)


@click.command()
@click.option('--version', '-v', help='Print version and exit.', is_flag=True)
@click.option('--format', '-f', help='Report format, default to txt', type=click.Choice(['txt', 'csv', 'json']), default='txt')
@click.option('--output', '-o', help='Output destination, default to stdout', default='stdout')
@click.option('--date', '-d', help='Date for which you want to retrieve metrics. Default for yesterday', type=click.DateTime(formats=['%m/%d/%Y']), default=datetime.strftime(datetime.now() + timedelta(days=-1), '%m/%d/%Y'))
@click.option('--log-file', '-f', help='Auth file to parse. Default to /var/log/auth.log', type=click.File('r'))
@click.option('--failed-passwords', help='Return statistics for failed passwords. Can be combined with --country-stats', is_flag=True)
@click.option('--invalid-users', help='Return statistics for invalid users. Can be combined with --country-stats', is_flag=True)
@click.option('--accepted-connections', help='Return statistics for accepted connections. Can be combined with --country-stats', is_flag=True)
@click.option('--country-stats', help='Return countries statistics.', is_flag=True)
def cli(**kwargs):
    """Retrieve metrics for SSH connections and generate reports"""
    if kwargs.get('version'):
        click.echo(f'Aeliant - SSH Metrics - Version {__version__}')
        sys.exit(0)

    day = datetime.strftime(kwargs.get('date'), '%b %d')
    REG = re.compile(r'{day}\s'.format(day=day) + MAIN_REGEX)

    ssh_auth = SSHAuth(day=day)
    for line in kwargs.get('log_file').readlines():
        match = REG.match(line)

        if match:
            if not ssh_auth.hostname:
                ssh_auth.hostname = match.group(2)
            ssh_auth.add_log(time=match.group(1), message=match.group(4))

    # generating report for failed passwords
    if kwargs.get('failed_passwords', False):
        report = ssh_auth.report(SSHAuth.FAILED_PASSWORDS, country_stats=kwargs.get('country_stats'), format=kwargs.get('format'))
        if kwargs.get('output') == 'stdout':
            print(report)
        else:
            _write_to_output(report, kwargs.get('output'), format=kwargs.get('format'))

    
    # generating report for invalid users
    if kwargs.get('invalid_users', False):
        report = ssh_auth.report(SSHAuth.INVALID_USERS, country_stats=kwargs.get('country_stats'), format=kwargs.get('format'))
        if kwargs.get('output') == 'stdout':
            print(report)
        else:
            _write_to_output(report, kwargs.get('output'), format=kwargs.get('format'))
    
    # generating report for accepted connections
    if kwargs.get('accepted_connections', False):
        report = ssh_auth.report(SSHAuth.ACCEPTED_CONNECTIONS, country_stats=kwargs.get('country_stats'), format=kwargs.get('format'))
        if kwargs.get('output') == 'stdout':
            print(report)
        else:
            _write_to_output(report, kwargs.get('output'), format=kwargs.get('format'))

