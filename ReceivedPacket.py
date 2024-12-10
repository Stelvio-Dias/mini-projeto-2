#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ReceivedPacket:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data

    def __eq__(self, other):
        if isinstance(other, ReceivedPacket):
            return self.seq_num == other.seq_num
        return False

    # Sobrescrevendo o método __hash__ para usar a marca como valor único
    def __hash__(self):
        return hash(self.seq_num)

    