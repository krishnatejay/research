
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
for lastDigits in range(1,101):
    partitions = partitions + ['10.0.0.' + str(lastDigits)  + '/255.255.0.127']

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
        removeFlowRules(ipAddress,macAddress,partition.split("/")[0]);
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
        distributionNumber = len(partitions)/len(currentlyActiveNodes) - len(partitions)/(len(currentlyActiveNodes)+1)
        activeNodeKeys = partitionMappings.keys()
        for key in activeNodeKeys:
		partitionsRebalanced = partitionMappings[key][-distributionNumber:]
		for partition in partitionsRebalanced:
		    keySplit = key.split('#')
		    removePartition(keySplit[0], keySplit[1], partition);
                    addPartition(ipAddress, macAddress, partition);

    currentlyActiveNodes = currentlyActiveNodes + [ipAddress + '#' + macAddress] 
    for key in partitionMappings.keys():
	print key + " : " + str(partitionMappings[key])

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


