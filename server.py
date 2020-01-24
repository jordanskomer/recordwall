import socket
import json
import time
import threading
import modes
from google import Intent
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import ssl

__clientid__ = 'recordwall'
__clientsecret__ = 'XQe4PXDUee8FpsQzRrk1L7P6ejRz2GXuFUs'
__token__= 'dfaashuihbniadAWEanuh23'

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if (self.path == '/'):
            self._set_headers()
            self.wfile.write(open('/home/pi/recordwall/index.html', 'rb').read())
        elif ('/google/auth' in self.path):
            query = urlparse(self.path).query
            params = dict(qc.split("=") for qc in query.split("&"))
            if (params['client_id'] == __clientid__):
                # Handle Oauth
                # https://oauth-redirect.googleusercontent.com/r/
                self.send_response(301)
                self.send_header(
                    'Location',
                    'https://oauth-redirect.googleusercontent.com/r/record-wall#access_token=%s&token_type=bearer&state=%s' % (__token__, params['state'])
                )
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()


    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
        if (self.path == '/google/intent'):
            intent = data['inputs'][0]['intent'].split('.')[2]
            print('New Intent %s' % intent)
            requestId = data['requestId']
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Authorization', 'Bearer %s' % __token__)
            self.end_headers()
            payload = Intent(intent, requestId, data)
            self.wfile.write(json.dumps(payload).encode('utf-8'))
        else:
            if (data['change']):
                # Adjust settings
                modes.adjust(int(data['brightness']), int(data['speed']))
            else:
                # Call Handler for passed in mode
                modes.Handler(data['mode'], data)
            self._set_headers()


def start_server(path, port):
    server = HTTPServer(('', port), Server)
    server.socket = ssl.wrap_socket(
        server.socket,
        certfile='/etc/letsencrypt/live/pi.jordanskomer.com/fullchain.pem',
        keyfile='/etc/letsencrypt/live/pi.jordanskomer.com/privkey.pem',
        server_side=True
    )
    print(time.asctime(), "Server Starts - %s:%s" % ('', port))
    # Set Default State
    server.serve_forever()
    # server.server_close()
    # print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

def start(port, background=False):
  # Run HTTP Server in Background
  daemon = threading.Thread(name='daemon_server', target=start_server, args=('.', port))
  if (background):
    daemon.setDaemon(True) # Set as a daemon so it will be killed once the main thread is dead.
  daemon.start()