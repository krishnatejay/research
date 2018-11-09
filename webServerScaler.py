import subprocess
import time

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        yield line

inActiveServers = []
activeWebServers = []

for i in range(11):
	end = str(i + 1)
	if(len(end) ==1):
		inActiveServers = ['10.3.0.10' + end] + inActiveServers
	else:
		inActiveServers = ['10.3.0.1' + end] + inActiveServers

def addNode():
	serverToBeAdded = inActiveServers.pop()
	print "Adding Node : " + str(serverToBeAdded)
	activeWebServers.append(serverToBeAdded)

def removeNode():
	if(len(activeWebServers) < 3):
		return
	serverToBeRemoved = activeWebServers.pop()
	print "Deleting Node : " + str(serverToBeRemoved)
	inActiveServers.append(serverToBeRemoved)

def dumpToFile(webServers):
	subprocess.call("rm -rf /home/ubuntu/research/tempWebServerConfig.txt",  shell=True)
	subprocess.call("touch  /home/ubuntu/research/tempWebServerConfig.txt",  shell=True)
	for server in webServers:
		subprocess.call("echo w " + str(server) + " >> /home/ubuntu/research/tempWebServerConfig.txt",  shell=True)
	subprocess.call("cat /home/ubuntu/research/tempWebServerConfig.txt > /home/ubuntu/research/webServerConfig.txt",  shell=True)

def handleLines(lines):
	totalRequestCount = 0
	for line in lines:
		value = int(line.split()[9])    
		totalRequestCount = totalRequestCount + value
		
	if(totalRequestCount > len(activeWebServers) * 21):
		i = len(activeWebServers) * 21
		#print "TotalRequstCount : " + str(totalRequestCount) + " counter : " + str(i)
		while(i<totalRequestCount):		
			addNode();
			i = i+21
		#	print "TotalRequstCount : " + str(totalRequestCount) + " counter : " + str(i)
	if(totalRequestCount < (len(activeWebServers) -1) * 21):
		nodesToBeRemoved = ((len(activeWebServers)) * 21 - totalRequestCount)/21;
		for i in range(nodesToBeRemoved):
			removeNode()
	dumpToFile(activeWebServers)

addNode()
addNode()
dumpToFile(activeWebServers)
logfile = open("/home/ubuntu/research/webServerLogs.txt","r")
loglines = follow(logfile)
lines = []
for line in loglines:
    lines = lines + [line]
    if(len(lines) < len(activeWebServers)):
   	 continue
    else:
	handleLines(lines)
        lines = []
