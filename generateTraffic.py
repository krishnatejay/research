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


for line in lines :
	parts = line.strip().split(",")
	if(parts[1] == "b"):
		bots = bots + [parts[0]]
	else:
		normalHosts = normalHosts + [parts[0]]

threads = []

def makeRequest(ipAddress):			
	process = Popen(["python", "session.py", ipAddress, "1.1.1.1"], stdout=PIPE)
	(output, err) = process.communicate()
	output = output.split('\n')
	matching = [s for s in output if "inet" in s]
	print ipAddress + " : " + str(matching)
	exit_code = process.wait()

def processTraffic(addressList):
	startTime = getEpochTime()
	endTime = startTime + 60 * len(trafficPatternLines)
	requestTracker = {}
	
	while(getEpochTime() < endTime ):
		currentMinute = (getEpochTime() - startTime)/5
		if(currentMinute == len(trafficPatternLines)):
			break;
		if(currentMinute not in requestTracker):
			print "Starting new Minute : " + str(currentMinute);
			requestTracker[currentMinute] = 0
		requestsInCurrentMinute = requestTracker[currentMinute] 
		if(requestsInCurrentMinute < int(trafficPatternLines[currentMinute].strip())):
			requestTracker[currentMinute] = requestTracker[currentMinute] + 1
			randNumber = random.randint(0,len(addressList))
			makeRequest(addressList[randNumber])
for i in range(1):
    process = Thread(target=processTraffic, args=[normalHosts])
    process.start()
    threads.append(process)	
for process in threads:
    process.join()



def makeRequest1(ipAddress):			
	print ipAddress