from numpy.random import seed
from numpy.random import randn
from numpy import percentile
import time
import subprocess


currentMinute = 0
def getOutliers(data):
	q25, q75 = percentile(data, 25), percentile(data, 75)
	iqr = q75 - q25
# calculate the outlier cutoff
	cut_off = iqr * 1.5
	lower, upper = q25 - cut_off, q75 + cut_off
# identify outliers
	outliers = [x for x in data if x < lower or x > upper]
	return outliers

#time.sleep(10)

def dumpToFile(anomalies):
	global currentMinute
	output = ""
	for anomaly in anomalies:
		output = output + anomaly +" " + currentMinute + "\n"
	subprocess.call("echo '"  + output[:-1] + "' >> /home/ubuntu/research/anomaly.txt",  shell=True)

while(True):
	global currentMinute
	time.sleep(59)
	with open("/home/ubuntu/research/ipStats.txt") as f:
		myList = list(f)
	if(len(myList) < 2):
		continue
	values = []
	lastLine = myList[len(myList)-1]
	currentMinute =  lastLine.split()[8]
	filteredList = []
	for line in myList:
		if(line.split()[8] == currentMinute):
			filteredList = [line] + filteredList
	myList = filteredList
	valueMappings = {}
	for line in myList:
		value = int(line.split()[14])
		if(value not in valueMappings.keys()):
			valueMappings[value] = []
		valueMappings[value] = [line.split()[5][:-1]] + valueMappings[value]
		values = values + [int(line.split()[14])]
	outLierValues = list(set(getOutliers(values)))

	outLiers = []
	for value in outLierValues:
		outLiers = outLiers + valueMappings[value]
	print outLiers
	dumpToFile(outLiers)
	
