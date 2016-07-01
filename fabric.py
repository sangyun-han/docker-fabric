#!/usr/bin/python

import os
import re
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, UserSwitch, Host
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI

class LeafSpine(Topo):
    def __init__(self, spine=2, leaf=2, fanout=2, **opts):
        "Create Leaf and Spine Topo."
        Topo.__init__(self, **opts)

        # Add spine switches
        spines = {}
        for s in range(spine):
            spines[s] = self.addSwitch('spine40%s' % (s + 1))
        # Set link speeds to 100Mb/s
        linkopts = dict(bw=10)

        # Add Leaf switches
        for ls in range(leaf):
            leafSwitch = self.addSwitch('leaf%s' % (ls + 1))
            # Connect leaf to all spines
            for s in range(spine):
                switch = spines[s]
                self.addLink(leafSwitch, switch, **linkopts)
            # Add hosts under a leaf, fanout hosts per leaf switch 
            for f in range(fanout):
                host = self.addHost('h%s' % (ls * fanout + f + 1),
                    cls=IpHost,  
                    ip='10.0.%s.%s/24' % ((ls + 1), (f + 1)),
                    gateway='10.0.%s.254' % (ls + 1))
                self.addLink(host, leafSwitch, **linkopts)

class IpHost(Host):
    def __init__(self, name, gateway, *args, **kwargs):
        super(IpHost, self).__init__(name, *args, **kwargs)
        self.gateway = gateway

    def config(self, **kwargs):
        Host.config(self, **kwargs)
        mtu = "ifconfig "+self.name+"-eth0 mtu 1490"
        self.cmd(mtu)
        self.cmd('ip route add default via %s' % self.gateway)


def init():
    spine = int(os.environ.get("FABRIC_SPINE", 2))
    leaf = int(os.environ.get("FABRIC_LEAF", 2))
    fanout = int(os.environ.get("FABRIC_FANOUT", 2))
    controllers = re.split(',', os.environ.get("FABRIC_CONTROLLER", "127.0.0.1"))
    topo = LeafSpine(spine=spine, leaf=leaf, fanout=fanout)
    net = Mininet(topo=topo, link=TCLink, build=False,
                  switch=UserSwitch,
                  controller = None,
                  autoSetMacs = True)
    for i in range(len(controllers)):
        if len(controllers[i]) != 0:
            net.addController("c%s" % i , controller=RemoteController, ip=controllers[i])

    net.build()
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    init()
    os.system('sudo mn -c')
