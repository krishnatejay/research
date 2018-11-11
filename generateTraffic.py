from subprocess import Popen, PIPE
import sys
from threading import Thread
import time
import random

def getEpochTime():
	seconds = int(round(time.time() ))
	return seconds

ipFile = sys.argv[1]
text_file = open(ipFile, "r")
lines = text_file.readlines()
trafficPatternFile = sys.argv[2]
trafficPatternFile = open(trafficPatternFile, "r")

trafficPatternLines = trafficPatternFile.readlines()
print trafficPatternLines

bots = []
normalHosts = []
hostMappings = {}


for line in lines :
	parts = line.strip().split(",")
	if(parts[1] == "b"):
		bots = bots + [parts[0]]
		hostMappings[parts[0]] = 'b'
	else:
		normalHosts = normalHosts + [parts[0]]
		hostMappings[parts[0]] = 'n'
	

threads = []

def makeRequest(ipAddress):
	url = "index.html"
	if(hostMappings[ipAddress] == 'b' or hostMappings[ipAddress] == 'bt'):
		url = "index1.html"	

	randNumber = random.randint(0,10000)
	if(hostMappings[ipAddress] == 'bt' and randNumber % 5 == 0):
		url = "doubleload.html"
	
	if(randNumber % 8 == 0 and hostMappings[ipAddress] != 'b'):
		url = "doubleload.html"			
	process = Popen(["python", "session.py", ipAddress, "10.2.0.115", url], stdout=PIPE)
	process1 = process
	if(hostMappings[ipAddress] == 'n' and randNumber % 6 == 0):
		process1 = Popen(["python", "session.py", ipAddress, "10.2.0.115", url], stdout=PIPE)
		(output, err) = process1.communicate()
	if(hostMappings[ipAddress] == 'b' and randNumber %5 == 0):
		process1 = Popen(["python", "session.py", ipAddress, "10.2.0.115", url], stdout=PIPE)
		(output, err) = process1.communicate()		
	(output, err) = process.communicate()
	#print ipAddress + " : " + str(matching)
	try:
		exit_code = process.wait()
		exit_code = process1.wait()
	except:
		print "Packet Handling Error"

def processTraffic(addressList):
	print len(addressList)
	startTime = getEpochTime()
	endTime = startTime + 60 * len(trafficPatternLines)
	requestTracker = {}
	
	while(getEpochTime() < endTime ):
		currentMinute = (getEpochTime() - startTime)/60
		if(currentMinute == len(trafficPatternLines)):
			break;
		if(currentMinute not in requestTracker):
			print "Starting new Minute : " + str(currentMinute);
			requestTracker[currentMinute] = 0
		requestsInCurrentMinute = requestTracker[currentMinute] 
		if(requestsInCurrentMinute < int(trafficPatternLines[currentMinute].strip())):
			requestTracker[currentMinute] = requestTracker[currentMinute] + 1
			randNumber = random.randint(0,len(addressList)-1)
			makeRequest(addressList[randNumber])
partitions = 4
for i in range(partitions):
    partitionSize = len(normalHosts)/partitions
    process = Thread(target=processTraffic, args=[normalHosts[i*partitionSize: (i+1) * partitionSize]])
    process.start()
    threads.append(process)
botPartitions = 2
for i in range(botPartitions):
    partitionSize = len(bots)/botPartitions
    if(i ==1):
	trafficBots = bots[i*partitionSize: (i+1) * partitionSize]
	for botIp in trafficBots:
		hostMappings[botIp] = 'bt'
    process = Thread(target=processTraffic, args=[bots[i*partitionSize: (i+1) * partitionSize]])
    process.start()
    threads.append(process)
	
for process in threads:
    process.join()



def makeRequest1(ipAddress):			
	print ipAddress
