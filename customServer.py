#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import socket
import commands
from threading import Thread
import time


def getEpochTime():
	seconds = int(round(time.time() ))
	return seconds

requestStats = {} 
startTime = getEpochTime()
value = str(commands.getstatusoutput('ifconfig | grep "inet" | grep "Bcast"')).strip().split('inet')[1].split(' ')[1]


def outputStats():

	while(True):
		currentMinute = (getEpochTime() - startTime)/60
		
		if(currentMinute-1 in requestStats.keys()):
			a =  "Bot Detector : " + str(value) + " Minute : " + str(currentMinute -1 ) + " Request Count : " + str(requestStats[currentMinute -1 ]['requests'])
			subprocess.call("echo '" + a +"' >> requestLogs.txt", shell=True)
			requestStats.pop(currentMinute - 1, None)
		time.sleep(60)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
	currentMinute = (getEpochTime() - startTime)/60
	if( currentMinute not in requestStats.keys()):
		requestStats[currentMinute] = {"requests" : 0, "dropped" : 0}
	requestStats[currentMinute]['requests'] = requestStats[currentMinute]['requests'] + 1
        self._set_headers()
        self.wfile.write("Ip Address : " + str(value) + "\n")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    process = Thread(target=outputStats)
    process.start()
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
