"""A set of configurations for diffecent possible feeds into the telemety
system. A feed will define the way the system is expected to listen on the
network to the data, and the different messages sent by the feed.
"""

import struct
import threading
import config
import socket


class UDPListener(threading.Thread):
    """A reusable UDP listener that sends incoming packes to a message reader"""

    def __init__(self, ip, port, reader):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.daemon = True
        self.queues = []
        self.reader = reader
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(0.01)

    def add_queue(self, q):
        self.queues.append(q)

    def run(self):
        while (not self._stop.is_set()):
            data = None
            try:
                data, addr = self.sock.recvfrom(config.PACKET_SIZE)
            except:
                pass

            if data is not None:
                obj = self.reader.decode_packet(data)
                for q in self.queues:
                    q.put(obj)

    def stop(self):
        self._stop.set()
        self.join()


class MessageReader(object):
    """A message reader class for PASA FC messages"""

    # This header is consistant across messages
    header = struct.Struct('!4sHLH')

    def __init__(self, messages):
        self.messages = messages
        self.compute_sizes()

    def compute_sizes(self):
        """Build a struct object based on the field definitions"""
        for message in self.messages:
            struct_string = self.messages[message]['endianness']
            for member in self.messages[message]['members']:
                struct_string += member['struct']
            self.messages[message]['struct'] = struct.Struct(struct_string)

    def decode_packet(self, packet):
        """A decoder for a packet"""

        # Loop until we've read the entire packet
        while len(packet) > 0:
            # Read header:
            fourcc, timestamp_hi, timestamp_lo, message_length = self.header.unpack(packet[:self.header.size])
            # fix timestamp
            timestamp = timestamp_hi << 32 | timestamp_lo
            # truncate what we've already read
            packet = packet[self.header.size:]

            # Debug
            #print fourcc, timestamp, message_length

            # Read body:
            # get message type from header
            message_type = self.messages.get(fourcc, None)
            if message_type is not None:

                # init a container for the values
                body = {'type': fourcc}

                # check to see if we read the right number of bytes
                if message_length != message_type['struct'].size:
                    # If the message isn't the right length, lets try and unpack
                    # it using the size of the struct.
                    message_length = message_type['struct'].size

                # read from packet
                unpacked = message_type['struct'].unpack(packet[:message_length])
                for i, field in enumerate(message_type['members']):
                    # get unit math
                    units = field.get('units', {})
                    shift = units.get('shift', 0)
                    scale = units.get('scale', 1)

                    # dump into dict
                    body[field['key']] = (unpacked[i] * scale) + shift

                # truncate what we've already read
                packet = packet[message_length:]

                # Debug
                yield body

## Definitions of feeds:

# Flight Computer
fc = {
    'listener': UDPListener,
    'ip': "",
    'port': 35001,
    'message_type': MessageReader,
    'messages': {
        'ADIS': {
            'endianness': '<',
            'members': [
                {'key': "VCC",     'struct': "h", 'units': {'mks': "volt", 'scale': 0.002418}},
                {'key': "Gryo_X",  'struct': "h", 'untis': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Y",  'struct': "h", 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gryo_Z",  'struct': "h", 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Acc_X",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 0.0333}},
                {'key': "Acc_Y",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 0.0333}},
                {'key': "Acc_Z",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 0.0333}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Temp",    'struct': "h", 'units': {'mks': "kelvin", 'scale': 0.14, 'shift': 273.15}},
                {'key': "Aux_ADC", 'struct': "h", 'units': {'mks': "volt", 'scale': 806}},
            ],
        },
        'ROLL': {
            'endianness': '<',
            'members': [
                {'key': "PWM", 'struct': "H", 'units': {'mks': "seconds", 'scale': 0}},
                {'key': "Disable", 'struct': "B"},
            ],
        },
    },
}

# List all active feeds
FEEDS = {
    'fc': fc,
}
