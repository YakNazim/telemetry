"""Statistics for Telemetry server"""

import time
from math import sqrt
import feeds


class PacketStats(object):
    """Can average multiple incoming packets before sending to frontend"""

    def __init__(self):
        self.data = {}

        # To differentiate incoming packet info we make a list of feeds
        self.packet_types = []
        for p in feeds.FEEDS.keys():
            self.packet_types.append('RECV_'+p)


    def append_data(self, incoming):
        """Called with a set of data from a thread. Should contain one
        message (many messages per packet)"""

        field_id = incoming.get('fieldID')

        # is this a seqn number?
        if field_id in self.packet_types:
            if field_id not in self.data:
                self.data[field_id] = {
                    'PacketsReceivedRecently': 1,
                    'LastSEQN': incoming.get('n', 0),
                    'TimeLastPacketReceived': incoming.get('recv', 0),
                    'PacketsLostRecently': 0,
                }
            else:
                last_seqn = self.data[field_id]['LastSEQN']
                this_seqn = incoming.get('n', 0)

                seqn_diff = this_seqn - last_seqn
                if seqn_diff == -1:
                    # out of order packet?
                    pass
                elif seqn_diff < -1:
                    # big shift?
                    pass
                elif seqn_diff > 1:
                    self.data[field_id]['PacketsLostRecently'] += seqn_diff

                self.data[field_id]['PacketsReceivedRecently'] += 1
                self.data[field_id]['LastSEQN'] = this_seqn
                self.data[field_id]['TimeLastPacketReceived'] = incoming.get('recv', 0)
            return


        if field_id not in self.data:
            # if we've not seen this before make it exist and init its numbers
            self.data[field_id] = {'count': 1}

            # safely get members
            d = incoming.get('recv', {})
            for key, val in d.iteritems():
                # Average number types
                if isinstance(val, float) or isinstance(val, int):
                    self.data[field_id][key+'_delta'] = val
                    self.data[field_id][key+'_mean'] = val
                    self.data[field_id][key+'_S'] = 0
                    self.data[field_id][key+'_sd'] = 0
                    self.data[field_id][key] = val
                else:
                    self.data[field_id][key] = val
        
        else:
            # Not the first instance of fieldID, so we append
            count = self.data[field_id]['count'] + 1
            self.data[field_id]['count'] = count
            d = incoming.get('recv', {})
            for key, val in d.iteritems():
                if isinstance(val, float) or isinstance(val, int):
                    # previous values
                    mean = self.data[field_id][key+'_mean']
                    delta = self.data[field_id][key+'_delta']
                    S = self.data[field_id][key+'_S']

                    # new values
                    delta = val - mean
                    mean += delta/float(count)
                    S += delta*(val - mean)
                    sd = sqrt(S/float(count))

                    # update
                    self.data[field_id][key+'_delta'] = delta
                    self.data[field_id][key+'_mean'] = mean
                    self.data[field_id][key+'_S'] = S
                    self.data[field_id][key+'_sd'] = sd
                    self.data[field_id][key] = val
                else:
                    types[field_id][key] = val

