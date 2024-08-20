import random

class NetworkLayer:
    def __init__(self, ip_src, ip_dest, transport_pdu):
        self.ip_src = ip_src
        self.ip_dest = ip_dest
        self.transport_pdu = transport_pdu
        self.packets_lost = 0
    
    def __repr__(self):
        return f"NetworkLayerPDU(ip_src={self.ip_src}, ip_dest={self.ip_dest}, transport_pdu={self.transport_pdu})"
    
    def check_ip(self, received_ip_src, received_ip_dest):
        return self.ip_src == received_ip_src and self.ip_dest == received_ip_dest

    # PDU: Packet
    def get_pdu(self):
        return {
            'ip_src': self.ip_src,
            'ip_dest': self.ip_dest,
            'transport_layer_pdu': self.transport_pdu
        }
    
    def to_transport_layer(self):
        return self.transport_pdu
    
    def simulate_packet_loss(self, loss_probability=0.1):
        for pdu in self.transport_pdu[:]:
            if random.random() < loss_probability:
                self.transport_pdu.remove(pdu)  # Eliminar el PDU si se "pierde"
                self.packets_lost += 1

        return self.packets_lost
