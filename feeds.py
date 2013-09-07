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
    """A message reader class for PASA FC messages"""

    # This header is consistant across messages
    header = struct.Struct('!4sHLH')

    def __init__(self, messages):
        self.messages = messages

    def decode_packet(self, packet):
        """A decoder for a packet"""

        # Read header
        fourcc, timestamp_hi, timestamp_lo, message_length = self.header.unpack(packet[:self.header.size])

        # fix timestamp
        timestamp = timestamp_hi << 32 | timestamp_lo

        # truncate what we've already read
        packet = packet[self.header.size:]
        print fourcc, timestamp, message_length

        # Read body
        # get message type from header
        message_type = self.messages.get(fourcc, None)
        if message_type is not None:

            # init a container for the values
            body = {'type': fourcc}
            message_size = 0

            # a temporary container for the body with a guess at the orginal lenght:
            body_packet = packet[:message_length]

            # Try to read through the fields as specified in the config
            for field in message_type.get('members', []):
                s = field['struct']

                try:
                    body[field['key']], = s.unpack(body_packet[:s.size])
                    message_size += s.size
                except:
                    #TODO: handle this case
                    pass
 
                # truncate what we already read
                body_packet = body_packet[s.size:]

            # check to see if we read the right number of bytes
            if message_length != message_size:
                print "Ahh!", message_length, message_size
            print body

# list of message types used in the message_type key
MESSAGE_TYPES = {
    'messages': MessageReader,
}
