import socket
import sys
import os
from DataPacket import DataPacket
import struct
import time

# Configurações
PACKET_SIZE = 1000
TIMEOUT = 1  # Em segundos

def file_sender(filename, server_ip, server_port, window_size):
    try:
        # Verifica se o arquivo existe
        if not os.path.isfile(filename):
            print("Erro: Arquivo não encontrado.")
            sys.exit(-1)

        # Cria socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(TIMEOUT)

        # Lê o arquivo
        with open(filename, "rb") as file:
            file_data = file.read()

        # Divide o arquivo em pedaços
        chunks = [file_data[i:i+PACKET_SIZE] for i in range(0, len(file_data), PACKET_SIZE)]
        total_chunks = len(chunks)
        print(f"Pedaços {total_chunks}")

        if (len(chunks[total_chunks - 1]) == PACKET_SIZE):
            chunks.append(b'')
            total_chunks = total_chunks + 1

        # Controle de envio
        base = 1  # Número de sequência do primeiro pedaço não confirmado
        next_seq_num = 1  # Próximo número de sequência a ser enviado
        acks_received = set()
        timeouts = 0

        print("Iniciando envio...")

        while base <= total_chunks:
            # Envia pacotes dentro da janela
            while next_seq_num < base + window_size and next_seq_num <= total_chunks:
                ##
                    # Envio
                checksum = calculate_simple_checksum(chunks[next_seq_num - 1])
                ##
                packet = DataPacket(next_seq_num, chunks[next_seq_num - 1], checksum)
                sock.sendto(packet.to_bytes(), (server_ip, int(server_port)))
                print(f"Enviado pacote {next_seq_num}")
                next_seq_num += 1

                if (next_seq_num == len(chunks)):
                    sock.sendto(DataPacket(0, b"eof", 0).to_bytes(), (server_ip, int(server_port)))

            try:
                # Recebe confirmações
                while True:
                    ack_data, _ = sock.recvfrom(PACKET_SIZE + 4)  # Recebe 1004 bytes (ack_pkt_t)

                    #PT
                    if len(ack_data) < 8:
                        print("ACK inválido recebido.")
                        continue

                    ack_seq, selective_acks = struct.unpack("II", ack_data)
                    
                    print(f"Recebido ACK {selective_acks}")

                    # Atualiza pacotes confirmados
                    if ack_seq >= base:
                        acks_received.add(selective_acks)
                    base = min(([i for i in range(base, total_chunks + 2) if i not in acks_received] or [total_chunks + 1]))

                    timeouts = 0

            except socket.timeout as e:
                # Reenvia pacotes não confirmados
                for seq_num in range(base, next_seq_num):
                    if seq_num not in acks_received:
                        print("Timeout! Reenviando pacotes pendentes...")
                        packet = DataPacket(seq_num, chunks[seq_num - 1], calculate_simple_checksum(chunks[seq_num - 1]))
                        sock.sendto(packet.to_bytes(), (server_ip, int(server_port)))
                        print(f"Reenviado pacote {seq_num}")

                if timeouts >= 3:   # Duvida de 3 ou 5, caso for para segundos ou tempo do timer
                    print("Erro: Muitos timeouts. Encerrando envio.")
                    sys.exit(-1)

        print("Envio concluído com sucesso.")
        sys.exit(0)

    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(-1)

def calculate_simple_checksum(data):
        # Calcula a soma dos valores dos bytes
        checksum = sum(data) % 256  # Garante que o checksum seja um único byte (0-255)
        return checksum

if __name__ == "__main__":
    if len(sys.argv) != 5:
       print("Uso: python file-sender.py <arquivo> <host> <porta> <tamanho_da_janela>")
       sys.exit(-1)

    filename = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = sys.argv[3]
    window_size = int(sys.argv[4])

    # filename = "sender/sended.txt"
    # server_ip = "localhost"
    # server_port = 12345
    # window_size = int(5)

    if window_size <= 0 or window_size > 32:
        print("ERRO! Tamanho da janela deve estar entre 1 e 32, saindo...")
        sys.exit(-1)

    file_sender(filename, server_ip, server_port, window_size)

