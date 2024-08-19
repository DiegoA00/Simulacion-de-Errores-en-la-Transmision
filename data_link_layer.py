from network_layer import NetworkLayer
import random

class DataLinkLayer:
    def __init__(self, mac_src, mac_dest, network_pdu:NetworkLayer):
        self.mac_src = mac_src
        self.mac_dest = mac_dest
        self.network_pdu = network_pdu
        self.fcs = self.calculate_crc()
        self.bits_changed = 0

    # funcion CRC simple para deteccion de errores
    def calculate_crc(self):
        frame = str(self.network_pdu.get_pdu())
        crc = 0
        for char in frame:
            crc ^= ord(char)
        return crc

    def get_crc(self):
        self.fcs
    
    def check_crc(self, received_crc):
        return self.fcs == received_crc
    
    def check_address(self, received_mac_src, received_mac_dest):
        return self.mac_src == received_mac_src and self.mac_dest == received_mac_dest
    
    def check_frame(self, received_mac_src, received_mac_dest, received_crc):
        return self.check_address(received_mac_src=received_mac_src, received_mac_dest=received_mac_dest) and self.check_crc(received_crc=received_crc)

    def to_network_layer(self):
        return self.network_pdu

    # PDU: Frame
    def get_pdu(self):
        return {
            'mac_src': self.mac_src,
            'mac_dest': self.mac_dest,
            'data': self.network_pdu.get_pdu(),
            'trailer': self.fcs
        }
    
    def simulate_bit_errors(self, error_rate=0.1):
        network_pdu_list = list(self.network_pdu.get_pdu())
        for i in range(len(network_pdu_list)):
            if random.random() < error_rate:
                self.bits_changed += 1
        return self.bits_changed
