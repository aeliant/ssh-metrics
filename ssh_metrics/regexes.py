"""@package ssh_metrics.regexes

All regexes used to parse SSH Auth. logs."""
import re

MAIN_REGEX = r'(0?[0-23]+:0?[0-59]+:0?[0-59]+)\s([^\s]*)\s+sshd\[(\d+)\]:\s*(.*)'
FAILED_PASS_REGEX = re.compile(r'Failed password.*user\s*([^\s]*).*from\s*([^\s]*)')
