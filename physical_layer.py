from data_link_layer import DataLinkLayer

class PhysicalLayer:
    def __init__(self, data_link_pdu:DataLinkLayer):
        self.data_link_pdu = data_link_pdu
        self.bits = self.convert_to_bits(data_link_pdu.get_pdu())
    
    def convert_to_bits(self, data):
        bits = ''
        for c in str(data):
            bits += (format(ord(c), '08b'))
        return bits

    def __repr__(self):
        return f"PhysicalLayerPDU(bitstream={self.bits[:50]}...)"
    
    def get_pdu(self):
        return {
            'bits': self.bits
        }
    
    def to_data_link_layer(self):
        return self.data_link_pdu

