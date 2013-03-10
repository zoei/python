'''
Created on 2012-11-27

@author: Zoei
'''
import sys, os, posixpath
import urllib.parse
import cgi
import shutil
import mimetypes
import re
import time
import resource
import http.server
import socketserver

CONFIG_DIR = '../../conf/'
WEB_CONFIG = CONFIG_DIR + 'server.ini'
config = resource.Configer(WEB_CONFIG).getparser()

server_conf = config['server']
SERVER_ADDR = (server_conf['host'], server_conf.getint('port'))
APP_BASE = os.sep.join(os.getcwd().split(os.sep)[:-2] + [config['app']['app.base']])

class EZHTTPRequsetHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        self.init_params()
        super().handle()

    def do_HEAD(self):
        super().do_HEAD()
        print('do_HEAD() start')

    def do_GET(self):
        print(self.parameters)
        try:
            super().do_GET()
            print('do_GET() start')
            shutil.copyfileobj(open(self.translate_path(self.path), 'rb'), self.wfile)
        except Exception as e:
            print(e)

    def translate_path(self, path):
        print(path)
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = APP_BASE
        for word in words:
            word = os.path.splitdrive(word)[1]
            word = os.path.split(word)[1]
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def init_params(self):
        self.parameters = {'host':self.address_string()}
        if "?" in self.path:
            for i in self.path.split("?")[1].split("&"):
                self.parameters[i.split("=")[0]] = urllib.parse.unquote_plus(i.split("=")[1])
            self.parameters["time"] = time.time()*1000;
        else:
            pass

def run(server_class=http.server.HTTPServer, handler_class=EZHTTPRequsetHandler):
    httpd = server_class(SERVER_ADDR, handler_class)
    httpd.serve_forever()
    
if __name__ == '__main__':
    sys.path.append('../../webapps/reviewboard/WEB-INF/py')
    exec('from reviewboard import test1 as a')
    print(a)
    #run()
