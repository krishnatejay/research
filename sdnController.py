
import time
import commands

currentlyActiveNodes = []
partitionMappings = {}

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        yield line

partitions = []


def addFlowRules(botdIpAddress , botdMacAddress, simulatedAddress):
   # botdIpAddress = "10.0.3.102";
   # botdMacAddress = "00:00:00:00:00:b2"
   # simulatedAddress = "10.0.1.101"
    clientIdentifier = int(simulatedAddress.split(".")[2])
    if(clientIdentifier <= 50):
        clientMacAddress = '00:00:00:00:0c:01';
    else:
        clientMacAddress = '00:00:00:00:0c:02'


    addFlow1 = "{\"dpid\": 64,\"idle_timeout\" : 10030,\"hard_timeout\" : 10030,\"priority\": 1113,\"match\":{   \"ipv4_src\" : \""+botdIpAddress+"\",   \"ipv4_dst\" : \""+simulatedAddress+"/255.255.0.127\",   \"eth_type\": 2048 },\"actions\":[    {        \"type\": \"SET_FIELD\",        \"field\": \"ipv4_src\",           \"value\": \"10.2.0.115\"             },    {        \"type\": \"SET_FIELD\",        \"field\": \"eth_dst\",           \"value\": \""+ clientMacAddress +"\"             },    {            \"type\":\"OUTPUT\",            \"port\": 1    }]}"
    addFlow2 = "{\"dpid\": 64,\"idle_timeout\" : 10030,\"hard_timeout\" : 10030,\"priority\": 1113,\"match\":{   \"ipv4_dst\" : \"10.2.0.115\",   \"ipv4_src\" : \""+simulatedAddress+"/255.255.0.127\",   \"eth_type\": 2048 },\"actions\":[       {        \"type\": \"SET_FIELD\",        \"field\": \"ipv4_dst\",           \"value\": \""+botdIpAddress+"\"             },    {        \"type\": \"SET_FIELD\",        \"field\": \"eth_dst\",           \"value\": \""+ botdMacAddress +"\"             },    {            \"type\":\"OUTPUT\",            \"port\": 2    }]}"
   
    status, output = commands.getstatusoutput("curl -X POST -i http://localhost:8080/stats/flowentry/add --data '" + addFlow1 + "'");
   # print status
   # print output
    status, output = commands.getstatusoutput("curl -X POST -i http://localhost:8080/stats/flowentry/add --data '" + addFlow2 + "'");
  #  print status
  #  print output

def removeFlowRules(botdIpAddress , botdMacAddress, simulatedAddress):
   # botdIpAddress = "10.0.3.102";
   # botdMacAddress = "00:00:00:00:00:b2"
   # simulatedAddress = "10.0.1.101"
    clientIdentifier = int(simulatedAddress.split(".")[2])
    if(clientIdentifier <= 50):
        clientMacAddress = '00:00:00:00:0c:01';
    else:
        clientMacAddress = '00:00:00:00:0c:02'


    addFlow1 = "{\"dpid\": 64,\"idle_timeout\" : 10030,\"hard_timeout\" : 10030,\"priority\": 1113,\"match\":{   \"ipv4_src\" : \""+botdIpAddress+"\",   \"ipv4_dst\" : \""+simulatedAddress+"/255.255.0.127\",   \"eth_type\": 2048 },\"actions\":[    {        \"type\": \"SET_FIELD\",        \"field\": \"ipv4_src\",           \"value\": \"10.2.0.115\"             },    {        \"type\": \"SET_FIELD\",        \"field\": \"eth_dst\",           \"value\": \""+ clientMacAddress +"\"             },    {            \"type\":\"OUTPUT\",            \"port\": 1    }]}"
    addFlow2 = "{\"dpid\": 64,\"idle_timeout\" : 10030,\"hard_timeout\" : 10030,\"priority\": 1113,\"match\":{   \"ipv4_dst\" : \"10.2.0.115\",   \"ipv4_src\" : \""+simulatedAddress+"/255.255.0.127\",   \"eth_type\": 2048 },\"actions\":[       {        \"type\": \"SET_FIELD\",        \"field\": \"ipv4_dst\",           \"value\": \""+botdIpAddress+"\"             },    {        \"type\": \"SET_FIELD\",        \"field\": \"eth_dst\",           \"value\": \""+ botdMacAddress +"\"             },    {            \"type\":\"OUTPUT\",            \"port\": 2    }]}"
   
    status, output = commands.getstatusoutput("curl -X POST -i http://localhost:8080/stats/flowentry/delete --data '" + addFlow1 + "'");
 #   print status
 #   print output
    status, output = commands.getstatusoutput("curl -X POST -i http://localhost:8080/stats/flowentry/delete --data '" + addFlow2 + "'");
 #   print status
 #   print output

# Defining all possible partitions. These will be distributed among the nodes approximately equally.
for lastDigits in range(1,21):
    partitions = partitions + ['10.0.0.' + str(lastDigits)  + '/255.255.0.127']

def addPartition(ipAddress, macAddress, partition):
        global partitionMappings
        ipMacKey = ipAddress + '#' + macAddress
#	print "Adding partition to ipaddress : " + ipAddress  + " partition : " + partition 
        addFlowRules(ipAddress,macAddress,partition.split("/")[0]);
        if (ipMacKey in partitionMappings.keys()):
            partitionMappings[ipMacKey] = partitionMappings[ipMacKey] + [partition]
        else:
            partitionMappings[ipMacKey] = [partition]			

def removePartition(ipAddress, macAddress, partition):
        global partitionMappings
        ipMacKey = ipAddress + '#' + macAddress
        removeFlowRules(ipAddress,macAddress,partition.split("/")[0]);
        partitionMappings[ipMacKey].remove(partition)
#	print "Removing partition to ipaddress : " + ipAddress  + " partition : " + partition
        

def handleNodeAddition(ipAddress, macAddress) :
    print "Adding Node ipAddress : "  + ipAddress + " macAddress: " + macAddress
    global currentlyActiveNodes
    global partitionMappings



    if(len(currentlyActiveNodes) == 0):
        for partition in partitions:
            addPartition(ipAddress, macAddress, partition)
            
    else:
	partitionsPerNode = len(partitions)/(len(currentlyActiveNodes)+1);
        distributionNumber = len(partitions)/len(currentlyActiveNodes) - len(partitions)/(len(currentlyActiveNodes)+1)
        activeNodeKeys = partitionMappings.keys()
        for key in activeNodeKeys:
		if(len(partitionMappings[key]) <= partitionsPerNode):
			continue; 
		partitionsRebalanced = partitionMappings[key][partitionsPerNode:]
		for partition in partitionsRebalanced:
		    keySplit = key.split('#')
   	            targetKey = ipAddress+'#' + macAddress;
		    if(targetKey in partitionMappings.keys() and len(partitionMappings[targetKey]) > partitionsPerNode):
			continue
		    removePartition(keySplit[0], keySplit[1], partition);
                    addPartition(ipAddress, macAddress, partition);

    currentlyActiveNodes = currentlyActiveNodes + [ipAddress + '#' + macAddress] 
    for key in partitionMappings.keys() :
	print str(key) + " : " + str(len(partitionMappings[key]))

def handleNodeDeletion(ipAddress, macAddress) :
    global partitionMappings
    print "Deleting Node ipAddress : "  + ipAddress + " macAddress: " + macAddress
    ipMacKey = ipAddress + '#' + macAddress
    activeNodes = partitionMappings.keys();
   # print activeNodes
  #  print ipMacKey
    activeNodes.remove(ipMacKey)
    index = 0
    movedPartitions = 0
    partitionsPerNode = (len(partitions)/(len(currentlyActiveNodes)-1)) + 1;
  #  print "Partitons per node : " + str(partitionsPerNode)
    partitionsToBeMoved = len(partitionMappings[ipMacKey])
    while(movedPartitions < partitionsToBeMoved):
        partition = partitionMappings[ipMacKey][0]
        currentKey = activeNodes[index%len(activeNodes)]
        currentKeySplit = currentKey.split('#')
	if(len(partitionMappings[currentKey]) < partitionsPerNode):
        	removePartition(ipAddress, macAddress, partition);
       		addPartition(currentKeySplit[0], currentKeySplit[1], partition);
	#	print "Remove Partitions : " + str(partition)
		movedPartitions = movedPartitions +1
	index = index + 1
    currentlyActiveNodes.remove(ipMacKey)
    partitionMappings.pop(ipMacKey, None)
    for key in partitionMappings.keys() :
	print str(key) + " : " + str(len(partitionMappings[key]))

nodeMappings = {}
availableNodes = []
for i in range(14):
	end = str(i + 1)
	if(len(end) ==1):
		nodeMappings['10.2.0.10' + end] = '00:00:00:00:0b:0' + end
	else:
		nodeMappings['10.2.0.1' + end] = '00:00:00:00:0b:' + end
availableNodes = nodeMappings.keys()	
	

def addNode():
	if(len(availableNodes) > 0 ):
		nodeSelected = availableNodes.pop()
		handleNodeAddition(nodeSelected, nodeMappings[nodeSelected])
		

def removeNode():
	if(len(partitionMappings.keys()) > 2):
		nodeSelected = partitionMappings.keys()[0]
		handleNodeDeletion(nodeSelected.split('#')[0], nodeMappings[nodeSelected.split('#')[0]])
		availableNodes.append(nodeSelected.split('#')[0])

def handleLines(lines):
	totalRequestCount = 0
	for line in lines:
		value = int(line.split()[10])    
		totalRequestCount = totalRequestCount + value
		
	if(totalRequestCount > len(partitionMappings.keys()) * 21):
		i = len(partitionMappings.keys()) * 21
		#print "TotalRequstCount : " + str(totalRequestCount) + " counter : " + str(i)
		while(i<totalRequestCount):		
			addNode();
			i = i+21
		#	print "TotalRequstCount : " + str(totalRequestCount) + " counter : " + str(i)
	if(totalRequestCount < (len(partitionMappings.keys()) -1) * 21):
		nodesToBeRemoved = ((len(partitionMappings.keys()) -1) * 21 - totalRequestCount)/21;
		for i in range(nodesToBeRemoved):
			removeNode()
		


addNode()
addNode()


logfile = open("/home/ubuntu/research/requestLogs.txt","r")
loglines = follow(logfile)
lines = []
for line in loglines:
    lines = lines + [line]
    if(len(lines) < len(partitionMappings.keys())):
   	 continue
    else:
	handleLines(lines)
        lines = []
    '''
    split = line.strip().replace('\n','').split(',')
    operation = split[0]
    ipAddress = split[1]
    macAddress = split[2]
    if (operation == 'Add'):
        print "Handling Node Addition : IpAddress = " + ipAddress + " Mac Address : " + macAddress
        handleNodeAddition(ipAddress, macAddress)
    else :
        print "Handling Node Deletion : IpAddress = " + ipAddress + " Mac Address : " + macAddress
        handleNodeDeletion(ipAddress, macAddress)
   '''


