"""A set of configurations for diffecent possible feeds into the telemety
system. A feed will define the way the system is expected to listen on the
network to the data, and the different messages sent by the feed.
"""

import struct
import threading
import config
import socket
import time


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
                if data is not None:
                    obj = self.reader.decode_packet(data)
                    for q in self.queues:
                        q.put(obj)
            except socket.timeout:
                pass

           
    def stop(self):
        self._stop.set()
        self.join()
        self.sock.close()



class MessageReader(object):
    """A message reader class for PSAS FC messages"""

    # This header is consistant across messages
    header = struct.Struct('!4sHLH')

    def __init__(self, messages):
        self.messages = messages
        self.compute_sizes()

    def compute_sizes(self):
        """Build a struct object based on the field definitions"""
        for message in self.messages:
            if self.messages[message]['type'] == "Fixed":
                struct_string = self.messages[message]['endianness']
                for member in self.messages[message]['members']:
                    struct_string += member['struct']
                self.messages[message]['struct'] = struct.Struct(struct_string)                

    def decode_packet(self, packet):
        """A decoder for a packet"""

        # packet header, sequence number
        seqn, = struct.unpack('!L', packet[0:4])
        packet = packet[4:]
        yield {'fieldID': 'SEQN', 'n': seqn, 'recv': time.time()}

        # Loop until we've read the entire packet
        while len(packet) > 0:
            # Read header:
            try:
                fourcc, timestamp_hi, timestamp_lo, message_length = self.header.unpack(packet[:self.header.size])
            except:
                print "Can't Read Header!!"
                break
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
                body = {'fieldID': fourcc}

                # Fixed lenght messages have a struct already
                st = message_type.get('struct', None)
                if st is not None:
                    # check to see if we read the right number of bytes
                    if message_length != st.size:
                        # If the message isn't the right length, lets try and unpack
                        # it using the size of the struct.
                        message_length = st.size
                else:
                    st = struct.Struct('%ds'%message_length)

                # read from packet
                try:
                    unpacked = st.unpack(packet[:message_length])
                except:
                    print "message read error"
                    packet = packet[message_length:]
                    continue
                for i, field in enumerate(message_type['members']):
                    # get unit math
                    units = field.get('units', None)
                    if units is not None:
                        shift = units.get('shift', 0)
                        scale = units.get('scale', 1)
                        # dump into dict
                        body[field['key']] = (unpacked[i] * scale) + shift
                    else:
                        body[field['key']] = unpacked[i]

                # Debug
                yield body
            else:
                print "skipped unkown header"

            # truncate what we've already read
            packet = packet[message_length:]

## Definitions of feeds:

# Flight Computer
fc = {
    'listener': UDPListener,
    'ip': "",
    'port': 35001,
    'message_type': MessageReader,
    'messages': {
        'ADIS': {
            'type': "Fixed",
            'endianness': '!',
            'members': [
                {'key': "VCC",     'struct': "h", 'units': {'mks': "volt", 'scale': 0.002418}},
                {'key': "Gyro_X",  'struct': "h", 'untis': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gyro_Y",  'struct': "h", 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Gyro_Z",  'struct': "h", 'units': {'mks': "hertz", 'scale': 0.05}},
                {'key': "Acc_X",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 0.0333}},
                {'key': "Acc_Y",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 0.0333}},
                {'key': "Acc_Z",   'struct': "h", 'units': {'mks': "meter/s/s", 'scale': 0.0333}},
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_Y",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Magn_Z",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.5}},
                {'key': "Temp",    'struct': "h", 'units': {'mks': "kelvin", 'scale': 0.14, 'shift': 273.15}},
                {'key': "Aux_ADC", 'struct': "h", 'units': {'mks': "volt", 'scale': 806}},
            ],
        },
        'ROLL': {
            'type': "Fixed",
            'endianness': '<',
            'members': [
                {'key': "PWM", 'struct': "H", 'units': {'mks': "seconds", 'scale': 0}},
                {'key': "Disable", 'struct': "B"},
            ],
        },
        'MPL3': {
            'type': "Fixed",
            'endianness': '<',
            'members': [
                {'key': "dummy1", 'struct': "L"},
                {'key': "dummy2", 'struct': "L"},
                #{'key': "dummy3", 'struct': "B"},
            ],
        },
        'MESG': {
            'type': "String",
            'members': [
                {'key': "Message", 'struct': "STRING"},
            ],
        },
    },
}

# List all active feeds
FEEDS = {
    'fc': fc,
}
