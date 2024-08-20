from physical_layer import PhysicalLayer
from data_link_layer import DataLinkLayer
from network_layer import NetworkLayer
from funciones import OSIModelSimulator

# direcciones IPs y MACs
original_ip_src = '192.168.1.100'
original_ip_dest = '192.168.1.120'
false_ip_src = '192.168.2.150'
false_ip_dest = '192.168.2.10'
mac_src = '00:1B:44:11:3A:B7'
false_mac_src = '00:1B:44:44:74:09'
mac_dest = '00:1B:44:11:3A:B7'
false_mac_dest = '00:1B:44:88:54:A1'

def encapsulation(data):
    print('Encapsulando...')
    # Capa de Apliacion
    simulation = OSIModelSimulator(data)
    application_pdu = simulation.application_layer()
    # Capa de Transporte
    transport_pdu = simulation.transport_layer(data=application_pdu, simulate_out_of_order=True)
    # Capa de Red
    print("Capa de Red: Convirtiendo en paquetes.")
    network_pdu = NetworkLayer(ip_src=original_ip_src, ip_dest=original_ip_dest, transport_pdu=transport_pdu)
    # Capa de Acceso a la Red
    print("Capa de Enlace de Datos: Convirtiendo en tramas.")
    data_link_pdu = DataLinkLayer(mac_src=mac_src, mac_dest=mac_dest, network_pdu=network_pdu)
    crc_generated = data_link_pdu.get_crc()
    print('Capa Fisica: Convirtiendo en bits')
    physical_pdu = PhysicalLayer(data_link_pdu=data_link_pdu)
    print('Encapsulado correctamente')
    return physical_pdu, crc_generated

def desencapsulation(physical_pdu:PhysicalLayer):
    # packets_lost, bits_changed = 0
    # data = ''
    # Capa de Acceso a la Red
    print('Desencapsulando...')
    data_link_pdu = physical_pdu.to_data_link_layer()
    # Simulacion cambios de bits
    bits_changed = data_link_pdu.simulate_bit_errors(error_rate=0.01)
    if not data_link_pdu.check_address(received_mac_src=mac_src, received_mac_dest=mac_dest):
        print('Error al desencapsular: direcciones MACs no coinciden(Capa: Acceso a la Red)')
        return 0, 0, 'Error'
    # Capa de Red
    network_pdu = data_link_pdu.to_network_layer()
    packets_lost = network_pdu.simulate_packet_loss(loss_probability=0.1)
    
    if not network_pdu.check_ip(received_ip_src=network_pdu.ip_src, received_ip_dest=network_pdu.ip_dest):
        print('Error al desencapsular: direcciones IPs no coinciden (Capa: Red)')
        return 0, 0, 'Error'
    # Capa de Transporte
    simulation = OSIModelSimulator(network_pdu)
    transport_pdu = simulation.transport_layer_receive(segments=network_pdu.to_transport_layer())

    data = simulation.application_layer_receive(data=transport_pdu)
    print('Desencapsulado correctamente')
    return packets_lost, bits_changed, data

if __name__ == "__main__":
    print('---Simulacion de Transmision---')
    
    data = input('Ingrese el mensaje: ')
    print('CLIENTE recibe: ', data, '\n')

    bits, original_crc = encapsulation(data)
    
    print('\nSERVIDOR')
    packets_lost, bits_changed, data = desencapsulation(bits)
    if data != 'Error':
        print('\nDurante la transmision del mensaje hubieron:')
        print(bits_changed, 'cambios de bits')
        print(packets_lost, 'paquetes perdidos')
        # Creacion del archivo
        with open('mensaje.txt', 'a') as file:
            data = data + '\n'
            file.write(data)
        print('Mensaje: ', data, '\nSe ha guardado en mensaje.txt')
