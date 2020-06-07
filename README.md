# SSH Metrics
[![Build Status](https://travis-ci.com/aeliant/ssh-metrics.svg?branch=master)](https://travis-ci.com/aeliant/ssh-metrics)

`ssh-metrics` is a python command line script allowing the user to read an SSH Auth. log file and return some metrics from it.

## Requirements
These are the following requirements (system wide) for the script to work:
*  geoip-bin

## Installation
You can install it from pypi:
```bash
pip install aeliant-ssh-metrics
```

## Basic usage
```bash
Usage: ssh-metrics [OPTIONS]

  Retrieve metrics for SSH connections and generate reports

Options:
  -f, --format [txt|csv|json]  Report format, default to txt
  -f, --output PATH            Output destination, default to /tmp
  -d, --date [%m/%d/%Y]        Date for which you want to retrieve metrics.
                               Default for yesterday

  -f, --log-file FILENAME      Auth file to parse. Default to
                               /var/log/auth.log

  --failed-passwords           Return statistics for failed passwords. Can be
                               prefixed with --country-stats

  --country-stats              Return countries statistics.
  --help                       Show this message and exit.

```

## Features
TODO