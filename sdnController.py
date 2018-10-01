
import time
import commands

currentlyActiveNodes = []
partitionMappings = {}
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

partitions = []


def addFlowRules(botdIpAddress , botdMacAddress, simulatedAddress):
   # botdIpAddress = "10.0.3.102";
   # botdMacAddress = "00:00:00:00:00:b2"
   # simulatedAddress = "10.0.1.101"
    clientIdentifier = int(simulatedAddress.split(".")[2])
    if(clientIdentifier <= 150):
        clientMacAddress = '00:00:00:00:00:c1';
    else:
        clientMacAddress = '00:00:00:00:00:c2'


    addFlow1 = "{\"dpid\": 64,\"idle_timeout\" : 10030,\"hard_timeout\" : 10030,\"priority\": 1113,\"match\":{   \"ipv4_src\" : \""+botdIpAddress+"/0.0.0.127\",   \"ipv4_dst\" : \""+simulatedAddress+"/0.0.0.127\",   \"eth_type\": 2048 },\"actions\":[    {        \"type\": \"SET_FIELD\",        \"field\": \"ipv4_src\",           \"value\": \"1.1.1.1\"             },    {        \"type\": \"SET_FIELD\",        \"field\": \"eth_dst\",           \"value\": \""+ clientMacAddress +"\"             },    {            \"type\":\"OUTPUT\",            \"port\": 1    }]}"
    addFlow2 = "{\"dpid\": 64,\"idle_timeout\" : 10030,\"hard_timeout\" : 10030,\"priority\": 1113,\"match\":{   \"ipv4_dst\" : \"1.1.1.1\",   \"ipv4_src\" : \""+simulatedAddress+"/0.0.0.127\",   \"eth_type\": 2048 },\"actions\":[       {        \"type\": \"SET_FIELD\",        \"field\": \"ipv4_dst\",           \"value\": \""+botdIpAddress+"\"             },    {        \"type\": \"SET_FIELD\",        \"field\": \"eth_dst\",           \"value\": \""+ botdMacAddress +"\"             },    {            \"type\":\"OUTPUT\",            \"port\": 2    }]}"
   
    status, output = commands.getstatusoutput("curl -X POST -i http://localhost:8080/stats/flowentry/add --data '" + addFlow1 + "'");
    print status
    print output
    status, output = commands.getstatusoutput("curl -X POST -i http://localhost:8080/stats/flowentry/add --data '" + addFlow2 + "'");
    print status
    print output

for lastDigits in range(101,102):
    partitions = partitions + ['0.0.0.' + str(lastDigits)  + '/0.0.0.127']

def addPartition(ipAddress, macAddress, partition):
        global partitionMappings
        ipMacKey = ipAddress + '#' + macAddress
	print "Adding partition to ipaddress : " + ipAddress  + " partition : " + partition 
        addFlowRules(ipAddress,macAddress,partition.split("/")[0]);
        if (ipMacKey in partitionMappings.keys()):
            partitionMappings[ipMacKey] = partitionMappings[ipMacKey] + [partition]
        else:
            partitionMappings[ipMacKey] = [partition]			

def removePartition(ipAddress, macAddress, partition):
        global partitionMappings
        ipMacKey = ipAddress + '#' + macAddress
        partitionMappings[ipMacKey].remove(partition)
	print "Removing partition to ipaddress : " + ipAddress  + " partition : " + partition
        

def handleNodeAddition(ipAddress, macAddress) :
    print "Adding Node ipAddress : "  + ipAddress + " macAddress: " + macAddress
    global currentlyActiveNodes
    global partitionMappings

    if(len(currentlyActiveNodes) == 0):
        for partition in partitions:
            addPartition(ipAddress, macAddress, partition)
            
    else:
        distributionNumber = (len(currentlyActiveNodes) *
                len(partitionMappings[partitionMappings.keys()[0]]))/(len(currentlyActiveNodes) + 1)
        activeNodeKeys = partitionMappings.keys()
        for key in activeNodeKeys:
		partitionsRebalanced = partitionMappings[key][-distributionNumber:]
		for partition in partitionsRebalanced:
		    keySplit = key.split('#')
		    removePartition(keySplit[0], keySplit[1], partition);
                    addPartition(ipAddress, macAddress, partition);

    currentlyActiveNodes = currentlyActiveNodes + [ipAddress + '#' + macAddress] 
    print partitionMappings

def handleNodeDeletion(ipAddress, macAddress) :
    global partitionMappings
    print "Deleting Node ipAddress : "  + ipAddress + " macAddress: " + macAddress
    ipMacKey = ipAddress + '#' + macAddress
    activeNodes = partitionMappings.keys();
    activeNodes.remove(ipMacKey)
    index = 0
    while(index < len(partitionMappings[ipMacKey])):
        partition = partitionMappings[ipMacKey][index]
        currentKey = activeNodes[index/len(activeNodes)]
        currentKeySplit = currentKey.split('#')
        removePartition(ipAddress, macAddress, partition);
        addPartition(currentKeySplit[0], currentKeySplit[1], partition);
    currentlyActiveNodes.remove(ipMacKey)
    partitionMappings.pop(ipMacKey, None)
    print partitionMappings
     

logfile = open("/home/ubuntu/research/sdnController.txt","r")
loglines = follow(logfile)
for line in loglines:
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


