from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg, info
from mininet.node import Node
from mininet.node import Host
from mininet.node import RemoteController
from mininet.topolib import TreeTopo
from mininet.util import waitListening
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
def sshd( network, cmd='/usr/sbin/sshd', opts='-D',
          ip='10.123.123.1/32', routes=None, switch=None ):
    """Start a network, connect it to root ns, and run sshd on all hosts.
       ip: root-eth0 IP address in root namespace (10.123.123.1/32)
       routes: Mininet host networks to route to (10.0/24)
       switch: Mininet switch to connect to root namespace (s1)"""
    print network
    if not switch:
        switch = network[ 's1' ]  # switch to use
    if not routes:
        routes = [ '10.0.0.0/24' ]
    connectToRootNS( network, switch, ip, routes )
    for host in network.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    info( "*** Waiting for ssh daemons to start\n" )
    for server in network.hosts:
        waitListening( server=server, port=22, timeout=5 )

    info( "\n*** Hosts are running sshd at the following addresses:\n" )
    for host in network.hosts:
        info( host.name, host.IP(), '\n' )
    info( "\n*** Type 'exit' or control-D to shut down network\n" )
    CLI( network )
    for host in network.hosts:
        host.cmd( 'kill %' + cmd )
    network.stop()


def startSetup():
    "Create and test a simple network"
    net = Mininet(topo=None,build=False)
    c1 = net.addHost( 'c1' , ip = '10.0.1.101/24',mac='00:00:00:00:00:c1')
    c2 = net.addHost( 'c2' , ip = '10.0.1.102/24',mac='00:00:00:00:00:c2')
    bd1 = net.addHost( 'bd1' , ip = '10.0.3.101/24',mac='00:00:00:00:00:b1')
    bd2 = net.addHost( 'bd2' , ip = '10.0.3.102/24',mac='00:00:00:00:00:b2')
    bd3 = net.addHost( 'bd3' , ip = '10.0.3.103/24',mac='00:00:00:00:00:b3')
    ws1 = net.addHost( 'ws1' , ip = '10.0.4.101/24',mac='00:00:00:00:00:f1')
    ws2 = net.addHost( 'ws2' , ip = '10.0.4.102/24',mac='00:00:00:00:00:f2')
    vs1 = net.addHost( 'vs1' , ip = '10.0.4.201/24',mac='00:00:00:00:00:f3')

    s1 = net.addSwitch( 's1' , listenPort=6633, protocols="OpenFlow13",
            dpid="0000000000000010")
    s2 = net.addSwitch( 's2' , listenPort=6633, protocols="OpenFlow13",
            dpid="0000000000000020")
    s3 = net.addSwitch( 's3' ,listenPort=6633,  protocols="OpenFlow13",
            dpid="0000000000000030")
    r1 = net.addSwitch( 'r1' , listenPort=6634, protocols="OpenFlow13",
            dpid="0000000000000040")
    r2 = net.addSwitch( 'r2' , listenPort=6634, protocols="OpenFlow13",
            dpid="0000000000000050")
    net.addLink( s1, c1 )
    net.addLink( s1, c2 )
    net.addLink( s2, bd1 )
    net.addLink( s2, bd2 )
    net.addLink( s2, bd3 )
    net.addLink( s3, ws1 )
    net.addLink( s3, ws2 )
    net.addLink( s3, vs1 )
    net.addLink( r1, s1 )
    net.addLink( r1, r2 )
    net.addLink( r2, s2 )
    net.addLink( r2, s3 )

    controller1 =net.addController("controller1",controller=RemoteController,ip="127.0.0.1",port=6633)
    controller2 =net.addController("controller2",controller=RemoteController,ip="127.0.0.1",port=6634)
    net.build()
    controller1.start()
    controller2.start()
    s1.start([controller1])
    s2.start([controller1])
    s3.start([controller1])
    r1.start([controller2])
    r2.start([controller2])
    CLI(net)
    net.stop()

def connectToRootNS( network, switch, ip, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    intf = network.addLink( root, switch ).intf1
    root.setIP( ip, intf=intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

#iprint topos
#sshd( MyTopo())
setLogLevel('info')
startSetup();