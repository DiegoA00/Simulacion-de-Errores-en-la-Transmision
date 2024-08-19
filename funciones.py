import random

class OSIModelSimulator:
    def __init__(self, file_content):
        self.file_content = file_content

    # Capa de Aplicación
    def application_layer(self):
        header = f"Filename: file.txt\nSize: {len(self.file_content)} bytes\n"
        data = header + self.file_content
        print("Capa de Aplicacion: Preparando los datos.")
        return data

    # Capa de Transporte
    def transport_layer(self, data, simulate_out_of_order=False):
        segment_size = 10  # tamaño de cada segmento
        segments = [data[i:i + segment_size] for i in range(0, len(data), segment_size)]
        
        # se les asigna un numero a los segmentos para poder ordenarlos luego
        segments = [(i, segment) for i, segment in enumerate(segments)]

        if simulate_out_of_order:
            random.shuffle(segments)  # Simula el envío fuera de orden
        
        print("Capa de Transporte: Segmentando los datos.")
        return segments

    # Capa de Red
    def network_layer(self, segments, simulate_packet_loss=False):
        ip_source = "192.168.1.1"
        ip_dest = "192.168.1.2"
        packets = []
        for seq, segment in segments:
            if simulate_packet_loss and random.random() < 0.01:
                print(f"Network Layer: Packet {seq} lost during transmission.")
                continue  # Simula la pérdida de paquetes
            packet = {
                "ip_source": ip_source,
                "ip_dest": ip_dest,
                "sequence": seq,
                "data": segment
            }
            packets.append(packet)
        print("Network Layer: Packets created with IP headers.")
        return packets

    # Capa de Enlace de Datos
    def data_link_layer(self, packets, simulate_data_corruption=False):
        mac_source = "AA:BB:CC:DD:EE:FF"
        mac_dest = "FF:EE:DD:CC:BB:AA"
        frames = []
        for packet in packets:
            checksum = sum(ord(char) for char in packet['data']) % 256
            if simulate_data_corruption and random.random() < 0.01:
                packet['data'] = packet['data'][:5] + 'X' + packet['data'][6:]  # Corrompe los datos
                print(f"Data Link Layer: Packet {packet['sequence']} corrupted.")
            frame = {
                "mac_source": mac_source,
                "mac_dest": mac_dest,
                "checksum": checksum,
                "data": packet
            }
            frames.append(frame)
        print("Data Link Layer: Frames created with MAC headers and checksum.")
        return frames

    # Capa Física
    def physical_layer(self, frames):
        signals = [frame for frame in frames]  # En una simulación real, esto convertiría los frames en señales eléctricas.
        print("Physical Layer: Data transmitted as signals.")
        return signals
    
    def transport_layer_receive(self, segments):
        # Ordenar los segmentos por el número de secuencia
        segments.sort(key=lambda x: x[0])
        
        # Reconstruir los datos
        reconstructed_data = ''.join(segment for _, segment in segments)
        return reconstructed_data

    def application_layer_receive(self, data):
            header, content = data.split('\n', 2)[1:]  # Elimina el encabezado
            return content

    # Recepción de datos en el Servidor
    def receive_data(self, signals):
        def physical_layer_receive(signals):
            print("Physical Layer: Signals received and converted back to frames.")
            return signals

        def data_link_layer_receive(frames):
            valid_packets = []
            for frame in frames:
                checksum = sum(ord(char) for char in frame['data']['data']) % 256
                if checksum == frame['checksum']:
                    valid_packets.append(frame['data'])
                else:
                    print(f"Data Link Layer: Frame {frame['data']['sequence']} discarded due to checksum error.")
            return valid_packets

        def network_layer_receive(packets):
            valid_segments = []
            for packet in packets:
                if packet['ip_dest'] == "192.168.1.2":  # Verifica la dirección IP de destino
                    valid_segments.append((packet['sequence'], packet['data']))
            return valid_segments

        def transport_layer_receive(segments):
            segments.sort()  # Reordena los segmentos en base al número de secuencia
            data = ''.join(segment for _, segment in segments)
            return data

        def application_layer_receive(data):
            header, content = data.split('\n', 2)[1:]  # Elimina el encabezado
            return content

        frames_received = physical_layer_receive(signals)
        packets_received = data_link_layer_receive(frames_received)
        segments_received = network_layer_receive(packets_received)
        data_reassembled = transport_layer_receive(segments_received)
        final_data = application_layer_receive(data_reassembled)
        print("Application Layer: Data received and reassembled.")
        return final_data

    

    # Simulación completa
    def simulate(self):
        data = self.application_layer()
        segments = self.transport_layer(data, simulate_out_of_order=True)
        packets = self.network_layer(segments, simulate_packet_loss=True)
        frames = self.data_link_layer(packets, simulate_data_corruption=True)
        signals = self.physical_layer(frames)
        
        received_file_content = self.receive_data(signals)

        # Verificar el contenido recibido
        print("\nOriginal file content:\n", self.file_content)
        print("\nReceived file content:\n", received_file_content)


# Uso de la clase
# file_content = "This is a test file content. We are testing the OSI model simulation."
# simulator = OSIModelSimulator(file_content)
# simulator.simulate()
