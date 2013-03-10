'''
Created on 2012-3-20

@author: hazh
'''
import BaseHTTPServer
import sys, os

WEB_ROOT = "/zoei/workspace/Python/poker/WebRoot"

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        response_file = WEB_ROOT + self.path
        try:
            if os.path.isfile(response_file):
                f = open(response_file, "r")
            elif os.path.isdir(response_file):
                f = open(response_file + "index.html", "r")
            else:
                self.send_error(404, "File not found")
                return
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # redirect stdout to client
            stdout = sys.stdout
            sys.stdout = self.wfile
            for line in f.readlines():
                print line
        finally:
            sys.stdout = stdout # restore

PORT = 80
httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()