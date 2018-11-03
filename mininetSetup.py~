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
    network
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
   
    c1 = net.addHost( 'c1' , ip = '10.0.0.101/16',mac='00:00:00:00:0c:01')
    c2 = net.addHost( 'c2' , ip = '10.0.0.102/16',mac='00:00:00:00:0c:02')
   
    bd1 = net.addHost( 'bd1' , ip = '10.2.0.101/16',mac='00:00:00:00:0b:01')
    bd2 = net.addHost( 'bd2' , ip = '10.2.0.102/16',mac='00:00:00:00:0b:02')
    bd3 = net.addHost( 'bd3' , ip = '10.2.0.103/16',mac='00:00:00:00:0b:03')
    bd4 = net.addHost( 'bd4' , ip = '10.2.0.104/16',mac='00:00:00:00:0b:04')
    bd5 = net.addHost( 'bd5' , ip = '10.2.0.105/16',mac='00:00:00:00:0b:05')
    bd6 = net.addHost( 'bd6' , ip = '10.2.0.106/16',mac='00:00:00:00:0b:06')
    bd7 = net.addHost( 'bd7' , ip = '10.2.0.107/16',mac='00:00:00:00:0b:07')
    bd8 = net.addHost( 'bd8' , ip = '10.2.0.108/16',mac='00:00:00:00:0b:08')
    bd9 = net.addHost( 'bd9' , ip = '10.2.0.109/16',mac='00:00:00:00:0b:09')
    bd10 = net.addHost( 'bd10' , ip = '10.2.0.110/16',mac='00:00:00:00:0b:10')
    bd11 = net.addHost( 'bd11' , ip = '10.2.0.111/16',mac='00:00:00:00:0b:11')
    bd12 = net.addHost( 'bd12' , ip = '10.2.0.112/16',mac='00:00:00:00:0b:12')
    bd13 = net.addHost( 'bd13' , ip = '10.2.0.113/16',mac='00:00:00:00:0b:13')
    bd14 = net.addHost( 'bd14' , ip = '10.2.0.114/16',mac='00:00:00:00:0b:14')
    bd15 = net.addHost( 'bd15' , ip = '10.2.0.115/16',mac='00:00:00:00:0b:15')

    ws1 = net.addHost( 'ws1' , ip = '10.3.0.101/16',mac='10:00:00:00:00:01')
    ws2 = net.addHost( 'ws2' , ip = '10.3.0.102/16',mac='10:00:00:00:00:02')
    ws3 = net.addHost( 'ws3' , ip = '10.3.0.103/16',mac='10:00:00:00:00:03')
    ws4 = net.addHost( 'ws4' , ip = '10.3.0.104/16',mac='10:00:00:00:00:04')
    ws5 = net.addHost( 'ws5' , ip = '10.3.0.105/16',mac='10:00:00:00:00:05')
    ws6 = net.addHost( 'ws6' , ip = '10.3.0.106/16',mac='10:00:00:00:00:06')
    ws7 = net.addHost( 'ws7' , ip = '10.3.0.107/16',mac='10:00:00:00:00:07')
    ws8 = net.addHost( 'ws8' , ip = '10.3.0.108/16',mac='10:00:00:00:00:08')
    ws9 = net.addHost( 'ws9' , ip = '10.3.0.109/16',mac='10:00:00:00:00:09')
    ws10 = net.addHost( 'ws10' , ip = '10.3.0.110/16',mac='10:00:00:00:00:10')



    vs1 = net.addHost( 'vs1' , ip = '10.3.0.201/16',mac='20:00:00:00:00:01')
    vs2 = net.addHost( 'vs2' , ip = '10.3.0.202/16',mac='20:00:00:00:00:02')
    vs3 = net.addHost( 'vs3' , ip = '10.3.0.203/16',mac='20:00:00:00:00:03')
    vs4 = net.addHost( 'vs4' , ip = '10.3.0.204/16',mac='20:00:00:00:00:04')
    vs5 = net.addHost( 'vs5' , ip = '10.3.0.205/16',mac='20:00:00:00:00:05')

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
    net.addLink( s2, bd4 )
    net.addLink( s2, bd5 )
    net.addLink( s2, bd6 )
    net.addLink( s2, bd7 )
    net.addLink( s2, bd8 )
    net.addLink( s2, bd9 )
    net.addLink( s2, bd10 )
    net.addLink( s2, bd11 )
    net.addLink( s2, bd12 )
    net.addLink( s2, bd13 )
    net.addLink( s2, bd14 )
    net.addLink( s2, bd15 )
 
    net.addLink( s3, ws1 )
    net.addLink( s3, ws2 )
    net.addLink( s3, ws3 )
    net.addLink( s3, ws4 )
    net.addLink( s3, ws5 )
    net.addLink( s3, ws6 )
    net.addLink( s3, ws7 )
    net.addLink( s3, ws8 )
    net.addLink( s3, ws9 )
    net.addLink( s3, ws10 )

    net.addLink( s3, vs1 )
    net.addLink( s3, vs2 )
    net.addLink( s3, vs3 )
    net.addLink( s3, vs4 )
    net.addLink( s3, vs5 ) 


    net.addLink( r1, s1 )
    net.addLink( r1, r2 )
    net.addLink( r2, s2 )
    net.addLink( r2, s3 )

    controller1 =net.addController("controller1",controller=RemoteController,ip="127.0.0.1",port=6633)
    controller2 =net.addController("controller2",controller=RemoteController,ip="127.0.0.1",port=6634)
    net.build()
    c1.cmd('route add default gw 10.0.0.103')
    c2.cmd('route add default gw 10.0.0.103')

    bd1.cmd('route add default gw 10.2.0.1')
    bd2.cmd('route add default gw 10.2.0.1')
    bd3.cmd('route add default gw 10.2.0.1')
    bd4.cmd('route add default gw 10.2.0.1')
    bd5.cmd('route add default gw 10.2.0.1')
    bd6.cmd('route add default gw 10.2.0.1')
    bd7.cmd('route add default gw 10.2.0.1')
    bd8.cmd('route add default gw 10.2.0.1')
    bd9.cmd('route add default gw 10.2.0.1')
    bd10.cmd('route add default gw 10.2.0.1')
    bd11.cmd('route add default gw 10.2.0.1')
    bd12.cmd('route add default gw 10.2.0.1')
    bd13.cmd('route add default gw 10.2.0.1')
    bd14.cmd('route add default gw 10.2.0.1')
    bd15.cmd('route add default gw 10.2.0.1')

    ws1.cmd('route add default gw 10.3.0.1')
    ws2.cmd('route add default gw 10.3.0.1')
    ws3.cmd('route add default gw 10.3.0.1')
    ws4.cmd('route add default gw 10.3.0.1')
    ws5.cmd('route add default gw 10.3.0.1')
    ws6.cmd('route add default gw 10.3.0.1')
    ws7.cmd('route add default gw 10.3.0.1')
    ws8.cmd('route add default gw 10.3.0.1')
    ws9.cmd('route add default gw 10.3.0.1')
    ws10.cmd('route add default gw 10.3.0.1')

    vs1.cmd('route add default gw 10.3.0.1')
    vs2.cmd('route add default gw 10.3.0.1')
    vs3.cmd('route add default gw 10.3.0.1')
    vs4.cmd('route add default gw 10.3.0.1')
    vs5.cmd('route add default gw 10.3.0.1')

    bd1.cmd('sudo python  customServer.py &')
    bd2.cmd('sudo python  customServer.py &')
    bd3.cmd('sudo python  customServer.py &')
    bd4.cmd('sudo python  customServer.py &')
    bd5.cmd('sudo python  customServer.py &')
    bd6.cmd('sudo python  customServer.py &')
    bd7.cmd('sudo python  customServer.py &')
    bd8.cmd('sudo python  customServer.py &')
    bd9.cmd('sudo python  customServer.py &')
    bd10.cmd('sudo python  customServer.py &')
    bd11.cmd('sudo python  customServer.py &')
    bd12.cmd('sudo python  customServer.py &')
    bd13.cmd('sudo python  customServer.py &')
    bd14.cmd('sudo python  customServer.py &')
    bd15.cmd('sudo python  customServer.py &')

    c1.cmd('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 10.2.0.101/24 -j DROP')
    c2.cmd('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 10.2.0.101/24 -j DROP')
    c1.cmd('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 1.1.1.1 -j DROP')
    c2.cmd('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 1.1.1.1 -j DROP')
    controller1.start()
    controller2.start()
    s1.start([controller1])
    s2.start([controller1])
    s3.start([controller1])
    r1.start([controller2])
    r2.start([controller2])
    return net

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
    #network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

#itopos
#sshd( MyTopo())
setLogLevel('info')
net = startSetup();
CLI(net)
net.stop()
