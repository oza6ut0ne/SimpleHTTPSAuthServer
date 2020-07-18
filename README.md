[![image](https://img.shields.io/pypi/pyversions/SimpleHTTPSAuthServer.svg)](https://pypi.org/project/SimpleHTTPSAuthServer/)

# SimpleHTTPSAuthServer

HTTPS server with Basic authentication and client certificate authentication.  
Supports both Python2 and Python3, IPv4 and IPv6.

## Installation

```sh
$ pip install SimpleHTTPSAuthServer
```

## Usage

```sh
# Serve HTTP.
$ python -m SimpleHTTPSAuthServer

# Serve HTTPS.
$ python -m SimpleHTTPSAuthServer -s /path/to/server/certificate.pem

# Serve HTTPS and enable client certificate authentication.
$ python -m SimpleHTTPSAuthServer -s /path/to/server/certificate.pem -c /path/to/CA/certificate.pem

# Enable Basic authentication.
# Create user 'foo' with password 'spam', and user 'bar' with password 'ham'.
$ python -m SimpleHTTPSAuthServer -u foo bar -p spam ham

# Environment variables are also available.
$ export SIMPLE_HTTPS_USERS='foo bar'
$ export SIMPLE_HTTPS_PASSWORDS='spam ham'

# Enable multi-thread.
$ python -m SimpleHTTPSAuthServer -t

# Specify listening port (default: 8000).
$ python -m SimpleHTTPSAuthServer 10080

# Bind to localhost only.
$ python -m SimpleHTTPSAuthServer -b 127.0.0.1

# Enable IPv6.
$ python -m SimpleHTTPSAuthServer -b ::
```
