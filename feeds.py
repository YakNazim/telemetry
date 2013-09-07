"""A set of configurations for diffecent possible feeds into the telemety
system. A feed will define the way the system is expected to listen on the
network to the data, and the different messages sent by the feed.
"""

import struct

# Flight Computer
fc = {
    'port_type': "UDP",
    'ip': "",
    'port': "35001",
    'message_type': "messages",
    'messages': {
        'ADIS': {
            'members': [
                {'key': "VCC",     'struct': struct.Struct("<h"), 'units': {'mks': "volt", 'scale': 2.418}},
                {'key': "Gryo_X",  'struct': struct.Struct("<h"), 'untis': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Y",  'struct': struct.Struct("<h"), 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Z",  'struct': struct.Struct("<h"), 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Acc_X",   'struct': struct.Struct("<h"), 'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Acc_Y",   'struct': struct.Struct("<h"), 'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Acc_Z",   'struct': struct.Struct("<h"), 'units': {'mks': "meter/s/s", 'scale': 3.33}},
                {'key': "Magn_X",  'struct': struct.Struct("<h"), 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'struct': struct.Struct("<h"), 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'struct': struct.Struct("<h"), 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Temp",    'struct': struct.Struct("<h"), 'units': {'mks': "kelvin", 'scale': 0.14}},
                {'key': "Aux_ADC", 'struct': struct.Struct("<h"), 'units': {'mks': "volt", 'scale': 806}},
            ],
        },
        'ROLL': {
            'members': [
                {'key': "PWM", 'struct': struct.Struct("H"), 'units': {'mks': "seconds", 'scale': 0}},
                {'key': "Disable", 'struct': struct.Struct("B")},
            ],
        },
    },
}

# List all active feeds
FEEDS = {
    'fc': fc,
}

class MessageReader(object):

    message_header = struct.Struct('!4sHLH')

    def __init__(self, messages):
        self.messages = messages

    def decode_packet(self, packet):

        # Read header
        s = self.message_header
        fourcc, timestamp_hi, timestamp_lo, length = s.unpack(packet[:s.size])
        timestamp = timestamp_hi << 32 | timestamp_lo
        packet = packet[s.size:]
        print fourcc, timestamp, length

        # read body
        message_type = self.messages.get(fourcc, None)
        if message_type is not None:
            body = {'type': fourcc}
            for field in message_type.get('members', []):
                s = field['struct']
                body[field['key']], = s.unpack(packet[:s.size])
                # truncate what we already read
                packet = packet[s.size:]
            print body

MESSAGE_TYPES = {
    'messages': MessageReader,
}
