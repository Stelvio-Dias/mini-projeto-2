import json
import socket
import sys
import struct
import os
from ReceivedPacket import ReceivedPacket

def main():
    ack_pkt_format = "II"
    received_pkts = set()
    buffer_size = 1024

    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        file_path = sys.argv[1]
        receiver_port = int(sys.argv[2])
        window_size = int(sys.argv[3])
    except IndexError:
        print("Erro na leitura de parametros. Status = -1")
        return


    try:
        receiver.bind(("localhost", receiver_port))
        print('Iniciado...')
    except Exception as e:
        print('\nNão foi possível iniciar! Status = -1\n', e)
        return
    authorized_sender = None

    base = None


    with open(file_path, "wb") as file:
        while True:
            try:
                data, address = receiver.recvfrom(buffer_size)
            except Exception as e:
                continue
        
            if authorized_sender is None:
                authorized_sender = address

            if address != authorized_sender:
                continue

            # Desfazer tupla
            try:
                num_seq, chunk, checksum = struct.unpack("!I1000sI", data)
            except Exception as e:
                print(f"Aconteceu uma escessao: {e}")
                continue
            
            if chunk == "eof":
                print("Entrei aqui")
                # Ordenar o set
                received_pkts_ordenados = sorted(received_pkts, key=lambda x: x.seq_num)

                # Escrever no ficheiro
                for packet in received_pkts_ordenados:
                    print(packet.seq_num)
                break

            if base is None:
                base = num_seq

            checksum2 = calculate_simple_checksum(chunk)

            if checksum == checksum2 and num_seq < (base + window_size):
                received_pkts.add(ReceivedPacket(num_seq, chunk))
                
                ack_pkt = struct.pack(ack_pkt_format, base, num_seq)
                receiver.sendto(ack_pkt, authorized_sender)

                if base == num_seq:
                    base += 1

            
            # ack_pkt = struct.pack(ack_pkt_format, base, base)
            # receiver.sendto(ack_pkt, authorized_sender)




    receiver.close()

    

## ----------------------------------------------------------------------------------

def calculate_simple_checksum(data):
        # Calcula a soma dos valores dos bytes
        checksum = sum(data) % 256  # Garante que o checksum seja um único byte (0-255)
        return checksum    


main()