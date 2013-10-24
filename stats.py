"""Statistics"""
import time


class PacketStats(object):

    def __init__(self):
        self.packets = 0
        self.last_seqn = 0
        self.last_packet_recv = time.time() #TODO: more sane init
        self.missed = 0
        self.seqn = 0
        self.this_packets = 0
        self.this_missed = 0
        self.this_droprate = 0
        self.this_rate = 0

    def run(self):
        self.this_packets = 0
        self.this_missed = 0
        self.this_droprate = 0
        self.this_rate = 0

    def packet(self, seqn, ts):
        self.seqn = seqn
        self.last_packet_recv = ts
        self.this_packets += 1
        self.packets += 1

        # computer missed packets
        if (seqn - self.last_seqn) > 1:
            self.this_missed += 1
            self.missed += 1

        self.this_droprate = self.this_missed/float(self.this_packets+self.this_missed) * 100 #%
        #self.this_rate = self.self.this_packets / 

        self.last_seqn = seqn
        self.last_packet_recv = ts
       
