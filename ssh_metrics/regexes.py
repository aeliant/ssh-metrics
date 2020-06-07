"""@package ssh_metrics.regexes

All regexes used to parse SSH Auth. logs."""
import re

# Only retrieving ssh logs
MAIN_REGEX = r'(?P<time>0?[0-23]+:0?[0-59]+:0?[0-59]+)\s(?P<hostname>[^\s]*)\s+sshd\[(\d+)\]:\s*(?P<message>.*)'

# Example: Failed password for invalid user yash from 80.211.7.53 port 48302 ssh2
FAILED_PASS_REGEX = re.compile(r'Failed password.*user\s*(?P<user>[^\s]*).*from\s*(?P<src_ip>[^\s]*)')

# Example: Invalid user yash from 80.211.7.53 port 48302
INVALID_USER_REGEX = re.compile(r'Invalid user (?P<user>[^\s]*).*from\s*(?P<src_ip>[^\s]*)')

# Example: Accepted publickey for darth.vader from 1.2.3.4 port 4444 ssh2: RSA SHA256:xxxxxxxx
# Example: Accepted password for darth.vader from 1.2.3.4 port 4444 ssh2
ACCEPTED_CONNECTION_REGEX = re.compile(r'Accepted\s*(?P<auth>publickey|password)\s*for\s*(?P<user>[^\s]*)\sfrom\s*(?P<src_ip>[^\s]*).*(ssh.*)')
