from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.icmp import icmp

log = core.getLogger()

class Final(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {}

    def do_final(self, packet, packet_in, port_on_switch, switch_id):
        eth = packet.find('ethernet')
        if not eth:
            return

        src_mac = str(eth.src)
        dst_mac = str(eth.dst)

        # Learn the port for the source MAC
        self.mac_to_port[src_mac] = port_on_switch

        # Check if the packet is an IPv4 packet
        if eth.type == ethernet.IP_TYPE:
            ip_header = packet.find(ipv4)
            if not ip_header:
                return

            src_ip = str(ip_header.srcip)
            dst_ip = str(ip_header.dstip)

            # Untrusted host rules
            if src_ip == '108.35.24.113':
                if (dst_ip.startswith('128.114.1.') or
                    dst_ip.startswith('128.114.2.') or
                    dst_ip == '128.114.3.178'):
                    self.drop_packet(packet, packet_in)
                    return  # Drop the packet

            # Trusted host rules
            if src_ip == '192.47.38.109':
                if (dst_ip.startswith('128.114.2.') or
                    dst_ip == '128.114.3.178'):
                    self.drop_packet(packet, packet_in)
                    return  # Drop the packet

            # Inter-department ICMP block
            if ip_header.protocol == ipv4.ICMP_PROTOCOL:
                if ((src_ip.startswith('128.114.1.') and dst_ip.startswith('128.114.2.')) or
                    (src_ip.startswith('128.114.2.') and dst_ip.startswith('128.114.1.'))):
                    self.drop_packet(packet, packet_in)
                    return  # Drop ICMP packets between departments

        # Install flow rule to forward packet to the known port
        if dst_mac in self.mac_to_port:
            out_port = self.mac_to_port[dst_mac]
            self.install_flow(packet, packet_in, out_port)
        else:
            self.flood_packet(packet_in, port_on_switch)

    def install_flow(self, packet, packet_in, out_port):
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, packet_in.in_port)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.data = packet_in
        self.connection.send(msg)

    def drop_packet(self, packet, packet_in):
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, packet_in.in_port)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
        msg.priority = 10
        self.connection.send(msg)

    def flood_packet(self, packet_in, in_port):
        msg = of.ofp_packet_out()
        msg.data = packet_in
        msg.in_port = in_port
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp
        self.do_final(packet, packet_in, event.port, event.dpid)

def launch():
    def start_switch(event):
        Final(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
