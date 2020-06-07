"""@package ssh_metrics.regexes

All regexes used to parse SSH Auth. logs."""
import re

MAIN_REGEX = r'(0?[0-23]+:0?[0-59]+:0?[0-59]+)\s([^\s]*)\s+sshd\[(\d+)\]:\s*(.*)'

# Failed password for invalid user yash from 80.211.7.53 port 48302 ssh2
FAILED_PASS_REGEX = re.compile(r'Failed password.*user\s*([^\s]*).*from\s*([^\s]*)')

# Invalid user yash from 80.211.7.53 port 48302
INVALID_USER_REGEX = re.compile(r'Invalid user ([^\s]*).*from\s*([^\s]*)')
