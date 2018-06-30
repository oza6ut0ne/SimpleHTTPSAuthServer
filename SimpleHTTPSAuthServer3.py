from http.server import SimpleHTTPRequestHandler, HTTPServer
import base64
import http
import itertools
import os
import random
import re
import ssl
import string


class AuthHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(http.client.UNAUTHORIZED)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Authorization Required\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_SUPERGET(self):
        super().do_GET()

    def do_GET(self):
        if self.server.noauth:
            if __name__ == '__main__':
                super().do_GET()
            return True

        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.do_AUTHHEAD()
            self.wfile.write('<h1>Authorization Required</h1>'.encode())
            print('no auth header received')
            return False

        elif auth_header[len('Basic '):] in self.server.keys:
            if __name__ == '__main__':
                super().do_GET()
            return True

        else:
            self.do_AUTHHEAD()
            self.wfile.write('<h1>Authorization Required</h1>'.encode())
            auth = re.sub('^Basic ', '', auth_header)
            print('Authentication failed! %s' % base64.b64decode(auth).decode())
            return False


class HTTPSAuthServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass=AuthHandler, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.noauth = False
        self.servercert = None
        self.cacert = None
        self.protocol = 'HTTP'
        self.certreqs = ssl.CERT_NONE

    def set_noauth(self, noauth):
        self.noauth = noauth

    def set_auth(self, users=[''], passwords=[''], keys=None):
        if keys is None:
            self.keys= []
            for user, password in itertools.zip_longest(users, passwords, fillvalue=''):
                self.keys.append(base64.b64encode(('%s:%s' % (user, password)).encode()).decode())
        else:
            self.keys = keys

    def set_certs(self, servercert=None, cacert=None):
        self.servercert = servercert
        self.cacert = cacert

        if servercert is not None:
            self.protocol = 'HTTPS'
            if cacert is not None:
                self.certreqs = ssl.CERT_REQUIRED

            self.socket = ssl.wrap_socket(self.socket, certfile=servercert,
                                          server_side=True,
                                          cert_reqs=self.certreqs,
                                          ca_certs=self.cacert)

    def serve_forever(self, poll_interval=0.5):
        if self.servercert is None:
            print('No server certificate is specified. Dropped to HTTP.')
        elif self.cacert is not None:
            print('CA certificate is specified. Now clients need cilent certificates.')

        sockname = self.socket.getsockname()
        print('Serving %s on %s port %s ...' % (self.protocol, sockname[0], sockname[1]))

        try:
            super().serve_forever(poll_interval)
        except KeyboardInterrupt:
            pass


def serve_https(address='', port=8000, noauth=False, users=[''], passwords=[''],
                keys=None, servercert=None, cacert=None, HandlerClass=AuthHandler):
    server = HTTPSAuthServer((address, port), HandlerClass)
    server.set_noauth(noauth)
    server.set_auth(users, passwords, keys)
    server.set_certs(servercert, cacert)
    server.serve_forever()


def random_string(length):
    return ''.join([random.choice(
        string.ascii_letters +
        string.digits +
        string.punctuation) for i in range(length)])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='An HTTPS server with Basic authentication '
                    'and client certificate authentication',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('port', nargs='?', type=int, default=8000)
    parser.add_argument('-a', '--address', default='')
    parser.add_argument('-n', '--noauth', action='store_true')
    parser.add_argument('-u', '--users', nargs='*', default=[''])
    parser.add_argument('-p', '--passwords', nargs='*', default=[''])
    parser.add_argument('-k', '--keys', nargs='*')
    parser.add_argument('-s', '--servercert')
    parser.add_argument('-c', '--cacert')
    parser.add_argument('-d', '--docroot')
    args = parser.parse_args()

    if args.servercert is not None:
        args.servercert = os.path.abspath(args.servercert)

    if args.cacert is not None:
        args.cacert = os.path.abspath(args.cacert)

    if args.docroot is not None:
        print('Set docroot to %s' % args.docroot)
        os.chdir(args.docroot)

    if not args.noauth and args.users == [''] and args.passwords == [''] and args.keys is None:
        args.users = [random_string(8)]
        args.passwords = [random_string(8)]
        print('Generated username and password -> %s : %s' % (args.users[0], args.passwords[0]))

    serve_https(args.address, args.port, args.noauth, args.users, args.passwords,
                args.keys, args.servercert, args.cacert)
