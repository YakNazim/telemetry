"""Statistics"""
import time
from math import sqrt

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


def filter(data):
    types = {}
    for d in data:
        if d['fieldID'] not in types:
            types[d['fieldID']] = {}
            types[d['fieldID']]['count'] = 1
            for key, val in d.iteritems():
                if isinstance(val, float) or isinstance(val, int):
                    types[d['fieldID']][key+'_delta'] = val
                    types[d['fieldID']][key+'_mean'] = val
                    types[d['fieldID']][key+'_S'] = 0
                    types[d['fieldID']][key+'_sd'] = 0
                    types[d['fieldID']][key] = val
                else:
                    types[d['fieldID']][key] = val
        else:
            types[d['fieldID']]['count'] += 1
            for key, val in d.iteritems():
                if isinstance(val, float) or isinstance(val, int):
                    types[d['fieldID']][key+'_delta'] = val - types[d['fieldID']][key+'_mean']
                    types[d['fieldID']][key+'_mean'] += types[d['fieldID']][key+'_delta']/float(types[d['fieldID']]['count'])
                    types[d['fieldID']][key+'_S'] += types[d['fieldID']][key+'_delta']*(val - types[d['fieldID']][key+'_mean'])
                    types[d['fieldID']][key+'_sd'] = sqrt(types[d['fieldID']][key+'_S']/float(types[d['fieldID']]['count']))
                    types[d['fieldID']][key] = val
                else:
                    types[d['fieldID']][key] = val
    return types

