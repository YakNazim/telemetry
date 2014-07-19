"""Statistics for Telemetry server"""

import time
from math import sqrt
import feeds

class PacketStats(object):
    """Can average multiple incoming packets before sending to frontend"""

    def __init__(self, last_seqn):
        self.data = {}
        self.last_seqn = last_seqn

        # To differentiate incoming packet info we make a list of feeds
        #self.packet_types = []
        #for p in feeds.FEEDS.keys():
        #    self.packet_types.append('RECV_'+p)


    def append_data(self, feed, incoming):
        """Called with a set of data from a thread. Should contain at least one
        message (many messages per packet)
        """

        # we got at least one packet
        if feed not in self.data:
            self.data[feed] = {
                'PacketsReceivedRecently': 0,
                'PacketsLostRecently': 0,
            }

        # go through data
        for d in incoming:
            for fourcc, msg in d.items():

                # is this a seqn number?
                if fourcc == 'SEQN':
                    this_seqn = msg.get('Sequence', 0)
                    seqn_diff = this_seqn - self.last_seqn
                    if seqn_diff == -1:
                        # out of order packet?
                        pass
                    elif seqn_diff < -1:
                        # big shift?
                        pass
                    elif seqn_diff > 1:
                        self.data[feed]['PacketsLostRecently'] += seqn_diff

                    self.last_seqn = this_seqn
                    self.data[feed]['PacketsReceivedRecently'] += 1
                    self.data[feed]['TimeLastPacketReceived'] = msg.get('recv', 0)
                else:

                    # first instance
                    if fourcc not in self.data[feed]:

                        self.data[feed][fourcc] = {'count': 1}

                        for key, val in msg.items():
                            # Average number types
                            if isinstance(val, float) or isinstance(val, int):
                                self.data[feed][fourcc][key+'_delta'] = val
                                self.data[feed][fourcc][key+'_mean'] = val
                                self.data[feed][fourcc][key+'_S'] = 0
                                self.data[feed][fourcc][key+'_sd'] = 0
                                self.data[feed][fourcc][key] = val
                            else:
                                self.data[feed][fourcc][key] = val

                    else:
                        # more than one:
                        count = self.data[feed][fourcc]['count'] + 1
                        self.data[feed][fourcc]['count'] = count

                        for key, val in msg.items():
                            if isinstance(val, float) or isinstance(val, int):
                                # previous values
                                mean = self.data[feed][fourcc][key+'_mean']
                                delta = self.data[feed][fourcc][key+'_delta']
                                S = self.data[feed][fourcc][key+'_S']

                                # new values
                                delta = val - mean
                                mean += delta/float(count)
                                S += delta*(val - mean)
                                sd = sqrt(S/float(count))

                                # update
                                self.data[feed][fourcc][key+'_delta'] = delta
                                self.data[feed][fourcc][key+'_mean'] = mean
                                self.data[feed][fourcc][key+'_S'] = S
                                self.data[feed][fourcc][key+'_sd'] = sd
                                self.data[feed][fourcc][key] = val
                            else:
                                self.data[feed][fourcc][key] = val
