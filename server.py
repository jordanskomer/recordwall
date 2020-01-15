import socket
import json
import time
import threading
from modes import Handler
from http.server import BaseHTTPRequestHandler, HTTPServer

__clientid__ = 'recordwall'
__clientsecret__ = 'XQe4PXDUee8FpsQzRrk1L7P6ejRz2GXuFUs'

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if (self.path == '/'):
            self._set_headers()
            self.wfile.write(open('/home/pi/recordwall/index.html', 'rb').read())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
        # Handle Google Home integration
        if (self.path == '/recordwall/ifttt'):
            status = data['status'].split()[0]
            print("Turning %s the record wall from IFTTT" % status)
            MODE = 'color' if status == 'on' else ''
        elif (self.path == '/google/auth'):
            print('Auth from google %d' % data)
        elif (self.path == '/google/token'):
            print('Token from google %d' % data)
        else:
            # Call Handler for passed in mode
            Handler(data['mode'], data)
        self._set_headers()


def start_server(path, port):
    server = HTTPServer(('', port), Server)
    print(time.asctime(), "Server Starts - %s:%s" % ('', port))
    # Set Default State
    Handler('color', json.loads('{ "r": "0", "g": "0", "b": "255", "mode": "color", "change": false, "loop": false }'))
    server.serve_forever()
    # server.server_close()
    # print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

def start(port, background=False):
  # Run HTTP Server in Background
  daemon = threading.Thread(name='daemon_server', target=start_server, args=('.', port))
  if (background):
    daemon.setDaemon(True) # Set as a daemon so it will be killed once the main thread is dead.
  daemon.start()