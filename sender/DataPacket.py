import struct

class DataPacket:
    def __init__(self, seq_num, data, checksum):
        self.seq_num = seq_num
        self.data = data
        self.checksum = checksum

    def to_bytes(self):
        """Converte para bytes para envio."""
        return struct.pack("!I1000sI", self.seq_num, self.data, self.checksum)

    @staticmethod
    def from_bytes(packet_bytes):
        """Converte bytes recebidos de volta para um objeto DataPacket."""
        seq_num, data = struct.unpack("!I1000sI", packet_bytes)
        return DataPacket(seq_num, data.rstrip(b'\x00'))