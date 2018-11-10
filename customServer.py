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
import requests 

def getEpochTime():
	seconds = int(round(time.time() ))
	return seconds

requestStats = {} 
startTime = getEpochTime()
value = str(commands.getstatusoutput('ifconfig | grep "inet" | grep "Bcast"')).strip().split('inet')[1].split(' ')[1]


webServers = []
verificationServers = []
ipStats = {}

def outputStats():
	global webServers
	global verificationServers

	while(True):
		linesList = []
                with open('/home/ubuntu/research/webServerConfig.txt') as f:
  			linesList = list(f)
		ws = []
		vs = []
		for line in linesList:
			parts = line.strip().split()
		
			if(parts[0] =='w' ):
				ws = [parts[1]] + ws
			if(parts[0] == 'v'):
				vs = [parts[1]] + vs
		webServers = ws
		verificationServers = vs
		print webServers
		print verificationServers
				
		currentMinute = (getEpochTime() - startTime)/60
		
		if(currentMinute-1 in requestStats.keys()):
			dropped = requestStats[currentMinute -1 ]['dropped']
			requests = requestStats[currentMinute -1 ]['requests']
			total = dropped + requests
			a =  "Bot Detector : " + str(value) + " Minute : " + str(currentMinute -1 ) + " Request Count : " + str(total) + " Success Count : " +  str(requests) + " Dropped : " + str(dropped)
			subprocess.call("echo '" + a +"' >> requestLogs.txt", shell=True)
			requestStats.pop(currentMinute - 1, None)
			currentStats = ipStats[currentMinute -1]
			output = ""
			for ip in currentStats:
				output = output + "Host : " + value + " Client : " + ip + ": currentMinute : " +  str(currentMinute -1) + " Requests : " + str(currentStats[ip]['requests']) + " Bytes : " +  str(currentStats[ip]['bytes']) + "\n"
			subprocess.call("echo '" + output[:-2] +"' >> ipStats.txt", shell=True)			
			ipStats.pop(currentMinute - 1, None)
		time.sleep(60)

index = 0
class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
	global index
	global ipStats
	index = index +1 
	currentMinute = (getEpochTime() - startTime)/60
	clientIp = self.client_address[0]
	if(currentMinute not in ipStats.keys()):
		ipStats[currentMinute] = {}
	if(clientIp not in ipStats[currentMinute].keys()):
		ipStats[currentMinute][clientIp] = {"requests": 0, "bytes" : 0}    
	if( currentMinute not in requestStats.keys()):
		requestStats[currentMinute] = {"requests" : 0, "dropped" : 0}
	if(requestStats[currentMinute]['requests'] > 20):
		requestStats[currentMinute]['dropped'] = requestStats[currentMinute]['dropped'] + 1
	else:
		if(clientIp not in ipStats[currentMinute].keys()):
			ipStats[currentMinute][clientIp] = {"requests": 0, "bytes" : 0} 
		requestStats[currentMinute]['requests'] = requestStats[currentMinute]['requests'] + 1
		ipStats[currentMinute][clientIp]['requests'] = ipStats[currentMinute][clientIp]['requests'] + 1
        self._set_headers()

	serverChoosed = webServers[index%len(webServers)]
	url = "http://" + serverChoosed
	r = requests.get(url = url) 

        self.wfile.write("Response : " + str(r.text) + "\n")

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
