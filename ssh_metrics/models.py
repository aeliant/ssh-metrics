"""@package ssh_metrics.models

Model used for storing SSH auth. infos."""
from subprocess import Popen, PIPE

from .regexes import FAILED_PASS_REGEX

class SSHAuth:
    """SSH Authentication model to be used for gathering metrics."""
    
    day = None
    hostname = None
    logs = []

    def __init__(self, **kwargs):
        """Initialize the SSHAuth object with the day and hostname."""
        self.day = kwargs.get('day', None)
        self.hostname = kwargs.get('hostname', None)

    def add_log(self, time, message):
        """Add a log to messages."""
        self.logs.append({
            'time': time,
            'message': message
        })
    
    @property
    def pretty_messages(self):
        return [f"{_.get('time')}: {_.get('message')}" for _ in self.logs]
    
    @property
    def failed_passwords(self):
        """Return metrics for failed password."""
        failed = []
        for message in self.logs:
            match = FAILED_PASS_REGEX.match(message.get('message'))
            if match:
                geoip_info = Popen(['geoiplookup', match.group(2)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, _ = geoip_info.communicate()
                failed.append({
                    'time': message.get('time'),
                    'user': match.group(1),
                    'src_ip': match.group(2),
                    'src_geoip': output.decode().split(':')[1].strip()
                })
        return failed