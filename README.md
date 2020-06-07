# SSH Metrics
[![Build Status](https://travis-ci.com/aeliant/ssh-metrics.svg?branch=master)](https://travis-ci.com/aeliant/ssh-metrics)

`ssh-metrics` is a python command line script allowing the user to read an SSH Auth. log file and return some metrics from it.

## Requirements
These are the following requirements (system wide) for the script to work:
*  `geoip-bin`

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
  -v, --version                Print version and exit.
  -f, --format [txt|csv|json]  Report format, default to txt
  -o, --output TEXT            Output destination, default to stdout
  -d, --date [%m/%d/%Y]        Date for which you want to retrieve metrics. If
                               not set, will scan for all the file without
                               filter.

  -f, --log-file FILENAME      Auth file to parse. Default to
                               /var/log/auth.log

  --failed-passwords           Return statistics for failed passwords. Can be
                               combined with --country-stats

  --invalid-users              Return statistics for invalid users. Can be
                               combined with --country-stats

  --accepted-connections       Return statistics for accepted connections. Can
                               be combined with --country-stats

  --country-stats              Return countries statistics.
  --help                       Show this message and exit.
```

## Features
All these example output are based with the `/var/log/auth.log` file.
Be sure of you're permissions before running it.

### Failed passwords
For a list of failed passwords:
```bash
$ ssh-metrics -d 05/17/2020 --failed-passwords --format txt
Time      User             Src ip           Src geoip
--------  ---------------  ---------------  ----------------------
00:00:15  yash             80.211.7.53      IT, Italy
00:02:42  apache2          203.135.20.36    PK, Pakistan
00:03:32  deploy           181.40.76.162    PY, Paraguay
00:03:43  ramya            99.245.133.108   CA, Canada
00:04:30  shubham          37.139.20.6      NL, Netherlands
00:04:33  gzw              195.231.0.89     IT, Italy
00:04:53  postgres         88.157.229.59    PT, Portugal
```

For the same list but with country statistics:
```bash
$ ssh-metrics -d 05/17/2020 --failed-passwords --format txt
GeoIP                     Count
----------------------  -------
IT, Italy                    26
PK, Pakistan                  1
PY, Paraguay                  3
CA, Canada                   22
NL, Netherlands              56
PT, Portugal                  3
```

## Invalid users
For a list of invalid users metrics:
```bash
$ ssh-metrics -d 05/17/2020 --invalid-users --format txt
Time      User             Src ip           Src geoip
--------  ---------------  ---------------  ----------------------
00:00:14  yash             80.211.7.53      IT, Italy
00:01:04  imran            195.231.0.89     IT, Italy
00:02:05  tuanna69         104.236.33.155   US, United States
00:02:40  apache2          203.135.20.36    PK, Pakistan
00:03:30  deploy           181.40.76.162    PY, Paraguay
00:03:41  ramya            99.245.133.108   CA, Canada
00:04:31  gzw              195.231.0.89     IT, Italy
00:04:51  postgres         88.157.229.59    PT, Portugal
00:05:11  hcn              176.31.102.37    FR, France
```

For the same list but with country statistics:
```bash
$ ssh-metrics -d 05/17/2020 --failed-passwords --format txt
GeoIP                     Count
----------------------  -------
IT, Italy                    26
PK, Pakistan                  1
PY, Paraguay                  3
CA, Canada                   22
NL, Netherlands              56
PT, Portugal                  3
```

## Accepted connections
For a list of accepted connections on your machine:
```bash
$ ssh-metrics -d 05/17/2020 --accepted-connections --format txt
Time      User     Auth       Src ip         Src geoip
--------  -------  ---------  -------------  -----------
10:53:19  yash     publickey  181.40.76.162  PY, Paraguay
10:53:19  imran    publickey  80.211.7.53    IT, Italy
10:53:19  apache2  publickey  203.135.20.36  PK, Pakistan
10:53:19  postgres publickey  176.31.102.37  FR, France
```

For the same list but with country statistics:
```bash
$ ssh-metrics -d 05/17/2020 --accepted-connections --format txt --country-stats

```
