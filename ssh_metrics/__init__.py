"""This script retrieve metrics of SSH connections for a given day."""
import click
import json
import re
import subprocess

from datetime import datetime, timedelta

FAILED_PASS_REGEX = re.compile(r'Failed password.*user\s*([^\s]*).*from\s*([^\s]*)')

class SSHAuth:
    day = None
    hostname = None
    messages = []

    def __init__(self, **kwargs):
        self.day = kwargs.get('day', None)
        self.hostname = kwargs.get('hostname', None)

    def add_log(self, time, message):
        self.messages.append({
            'time': time,
            'message': message
        })
    
    @property
    def pretty_messages(self):
        return [f"{_.get('time')}: {_.get('message')}" for _ in self.messages]
    
    @property
    def failed_passwords(self):
        """Return metrics for failed password."""
        failed = []
        for message in self.messages:
            match = FAILED_PASS_REGEX.match(message.get('message'))
            if match:
                geoip_info = subprocess.Popen(['geoiplookup', match.group(2)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, _ = geoip_info.communicate()
                failed.append({
                    'time': message.get('time'),
                    'user': match.group(1),
                    'src_ip': match.group(2),
                    'src_geoip': output.decode().split(':')[1].strip()
                })
        return failed


@click.command()
@click.option('--format', '-f', help='Report format, default to txt', type=click.Choice(['txt', 'csv', 'json']), default='txt')
@click.option('--output', '-f', help='Output destination, default to /tmp', type=click.Path(exists=True), default='/tmp')
@click.option('--date', '-d', help='Date for which you want to retrieve metrics. Default for yesterday', type=click.DateTime(formats=['%m/%d/%Y']), default=datetime.strftime(datetime.now() + timedelta(days=-1), '%m/%d/%Y'))
@click.option('--log-file', '-f', help='Auth file to parse. Default to /var/log/auth.log', type=click.File('r'), default='/var/log/auth.log')
@click.option('--failed-passwords', help='Return statistics for failed passwords. Can be prefixed with --country-stats', is_flag=True)
@click.option('--country-stats', help='Return countries statistics.', is_flag=True)
def cli(**kwargs):
    """Retrieve metrics for SSH connections and generate reports"""
    day = datetime.strftime(kwargs.get('date'), '%b %d')
    MAIN_REGEX = re.compile(r'{day}\s(0?[0-23]+:0?[0-59]+:0?[0-59]+)\s([^\s]*)\s+sshd\[(\d+)\]:\s*(.*)'.format(day=day))

    ssh_auth = SSHAuth(day=day)
    for line in kwargs.get('log_file').readlines():
        match = MAIN_REGEX.match(line)

        if match:
            if not ssh_auth.hostname:
                ssh_auth.hostname = match.group(2)
            ssh_auth.add_log(time=match.group(1), message=match.group(4))

    if kwargs.get('failed_passwords', False):
        failed_passwords = ssh_auth.failed_passwords
        