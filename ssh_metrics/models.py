"""@package ssh_metrics.models

Model used for storing SSH auth. infos."""
import inflection

from tabulate import tabulate
from subprocess import Popen, PIPE

from .regexes import FAILED_PASS_REGEX, INVALID_USER_REGEX

class SSHAuth:
    """SSH Authentication model to be used for gathering metrics."""

    FAILED_PASSWORDS = 0
    INVALID_USERS = 1
    
    day = None
    hostname = None
    logs = None

    def __init__(self, **kwargs):
        """Initialize the SSHAuth object with the day and hostname."""
        self.day = kwargs.get('day', None)
        self.hostname = kwargs.get('hostname', None)
        self.logs = []

    def add_log(self, time, message):
        """Add a log to messages."""
        self.logs.append({
            'time': time,
            'message': message
        })
    
    @property
    def pretty_messages(self):
        return [f"{_.get('time')}: {_.get('message')}" for _ in self.logs]
    
    def failed_passwords(self, country_stats=False):
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
        
        if country_stats:
            stats = {}
            for element in failed:
                if element.get('src_geoip') in stats:
                    stats[element.get('src_geoip')] += 1
                else:
                    stats[element.get('src_geoip')] = 1
            return stats

        return failed
    
    def invalid_users(self, country_stats=False):
        """Return metrics for invalid users."""
        failed = []
        for message in self.logs:
            match = INVALID_USER_REGEX.match(message.get('message'))
            if match:
                geoip_info = Popen(['geoiplookup', match.group(2)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, _ = geoip_info.communicate()
                failed.append({
                    'time': message.get('time'),
                    'user': match.group(1),
                    'src_ip': match.group(2),
                    'src_geoip': output.decode().split(':')[1].strip()
                })
        
        if country_stats:
            stats = {}
            for element in failed:
                if element.get('src_geoip') in stats:
                    stats[element.get('src_geoip')] += 1
                else:
                    stats[element.get('src_geoip')] = 1
            return stats
        
        return failed
    
    def _gen_report(self, data, format, country_stats):
        """For a given set of data, format and country_stats, return the corresponding report."""
        # first checking if any data
        if len(data) == 0:
            return data
        
        # checking format
        if format == 'json':
            return data
        elif format == 'txt':
            if country_stats:
                headers = ['GeoIP', 'Count']
                to_return = data.items()
                return tabulate(to_return, headers=headers)
            else:
                headers = [inflection.humanize(_) for _ in data[0].keys()]
                to_return = [
                    [value for key, value in _.items()]
                    for _ in data
                ]
                return tabulate(to_return, headers=headers)
        elif format == 'csv':
            if country_stats:
                headers = ['GeoIP', 'Count']
                to_return = [';'.join([key, str(value)]) for key, value in data.items()]
                return ';'.join(headers) + '\n' + '\n'.join(to_return)
            else:
                headers = [inflection.humanize(_) for _ in data[0].keys()]
                to_return = [
                    ';'.join([value for key, value in _.items()])
                    for _ in data
                ]
                return ';'.join(headers) + '\n' + '\n'.join(to_return)
        else:
            return None
    
    def report(self, metric_type, country_stats=False, format='json'):
        """Generate a report content for the specified type and format.
        
        Valid formats:
        *  json
        *  csv
        *  txt

        Valid metric types:
        *  failed_passwords
        *  invalid_users

        If format or metric_type is not recognized, return None
        """
        if metric_type == self.FAILED_PASSWORDS:
            stats = self.failed_passwords(country_stats=country_stats)
            data = self._gen_report(stats, format=format, country_stats=country_stats)
        elif metric_type == self.INVALID_USERS:
            stats = self.invalid_users(country_stats=country_stats)
            data = self._gen_report(stats, format=format, country_stats=country_stats)
        else:
            return None
        
        return data
    
    def failed_passwords_report(self, country_stats=False, format='json'):
        """Generate a report content with the specified format for failed passwords.

        Valid formats:
        *  json
        *  csv
        *  txt
        
        If format is not recognized, return None"""
        if format == 'json':
            return self.failed_passwords(country_stats=country_stats)
        elif format == 'csv':
            stats = self.failed_passwords(country_stats=country_stats)
            if country_stats:
                headers = ['GeoIP', 'Count']
                data = [';'.join([key, str(value)]) for key, value in stats.items()]
                return ';'.join(headers) + '\n' + '\n'.join(data)
            else:
                headers = [inflection.humanize(_) for _ in stats[0].keys()]
                data = [
                    ';'.join([value for key, value in _.items()])
                    for _ in stats
                ]
                return ';'.join(headers) + '\n' + '\n'.join(data)
        elif format == 'txt':
            stats = self.failed_passwords(country_stats=country_stats)
            if len(stats) == 0:
                return []

            if country_stats:
                headers = ['GeoIP', 'Count']
                data = stats.items()
                return tabulate(data, headers=headers)
            else:
                print(stats)
                headers = [inflection.humanize(_) for _ in stats[0].keys()]
                data = [
                    [value for key, value in _.items()]
                    for _ in stats
                ]
                return tabulate(data, headers=headers)
        else:
            return None