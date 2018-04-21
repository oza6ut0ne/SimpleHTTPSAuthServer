from http.server import SimpleHTTPRequestHandler, HTTPServer
import base64
import os
import random
import re
import ssl
import string


class AuthHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Authorization Required\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

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

        elif auth_header == 'Basic ' + self.server.key:
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
        self.cert = None
        self.protocol = 'HTTP'

    def set_noauth(self, noauth):
        self.noauth = noauth

    def set_auth(self, user='', password='', key=None):
        if key is None:
            self.key = base64.b64encode(('%s:%s' % (user, password)).encode()).decode()
        else:
            self.key = key

    def set_cert(self, cert):
        self.cert = cert
        if cert is not None:
            self.protocol = 'HTTPS'
            self.socket = ssl.wrap_socket(self.socket, certfile=cert, server_side=True)

    def serve_forever(self, poll_interval=0.5):
        if self.cert is None:
            print('No certfile is specified. Dropped to HTTP.')

        sockname = self.socket.getsockname()
        print('Serving %s on %s port %s ...' % (self.protocol, sockname[0], sockname[1]))
        
        try:
            super().serve_forever(poll_interval)
        except KeyboardInterrupt:
            pass


def serve_https(address='', port=8000, noauth=False, user='', password='',
                key=None, certfile=None, HandlerClass=AuthHandler):
    server = HTTPSAuthServer((address, port), HandlerClass)
    server.set_noauth(noauth)
    server.set_auth(user, password, key)
    server.set_cert(certfile)
    server.serve_forever()


def random_string(length):
    return ''.join([random.choice(
        string.ascii_letters +
        string.digits +
        string.punctuation) for i in range(length)])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='HTTPS server with Basic authentication.')
    parser.add_argument('port', nargs='?', type=int, default=8000)
    parser.add_argument('-a', '--address', default='')
    parser.add_argument('-n', '--noauth', action='store_true')
    parser.add_argument('-u', '--user', default='')
    parser.add_argument('-p', '--password', default='')
    parser.add_argument('-k', '--key')
    parser.add_argument('-c', '--cert')
    parser.add_argument('-d', '--docroot')
    args = parser.parse_args()

    if args.cert is not None:
        args.cert = os.path.abspath(args.cert)

    if args.docroot is not None:
        print('Set docroot to %s' % args.docroot)
        os.chdir(args.docroot)

    if not args.noauth and args.user == '' and args.password == '' and args.key is None:
        args.user = random_string(8)
        args.password = random_string(8)
        print('Generated username and password -> %s : %s' % (args.user, args.password))

    serve_https(args.address, args.port, args.noauth, args.user, args.password, args.key, args.cert)

