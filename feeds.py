"""A set of configurations for diffecent possible feeds into the telemety
system. A feed will define the way the system is expected to listen on the
network to the data, and the different messages sent by the feed.
"""

import struct
import threading
import config
import socket
import time
import gps


################################################################################
# LISTENER CLASSES
################################################################################
class Listener(threading.Thread):
    """Abstract listener class"""

    def __init__(self, reader):
        """Init thread"""
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.daemon = True
        self.queues = []
        self.reader = reader

    def add_queue(self, q):
        """Must accept a queue during initilaztion in main thread"""
        self.queues.append(q)

    def run(self):
        """begin thread"""
        while (not self._stop.is_set()):
            self.thread()

    def stop(self):
        """Stop thread"""
        self._stop.set()
        self.join()
        self.sock.close()

    def thread(self):
        """Override this to add functionality to a thread"""
        pass


class UDPListener(Listener):
    """A reusable UDP listener that sends incoming packes to a message reader"""

    def __init__(self, args, reader):
        super(UDPListener, self).__init__(reader)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((args['ip'], args['port']))
        self.sock.settimeout(0.01)


    def thread(self):
        data = None
        try:
            data, addr = self.sock.recvfrom(config.PACKET_SIZE)
            if data is not None:
                obj = self.reader.decode_packet(data)
                for q in self.queues:
                    q.put(obj)
        except socket.timeout:
            pass


class GPSConst(Listener):
    """A GPS Constilation Renderer"""

    def __init__(self, args, reader):
        super(GPSConst, self).__init__(reader)
        # Init sat data
        self.sats = gps.init_constellation()

    def thread(self):
        # compute gps positions
        if self.sats is not None:
            data = gps.compute(self.sats)
            obj = self.reader.make_messages(data)
            if obj is not None:
                for q in self.queues:
                    q.put(obj)
        time.sleep(1)


################################################################################
# MESSAGE CLASSES
################################################################################
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

        # TODO: fix hardcoded message type!!!!
        yield {'fieldID': 'RECV_fc', 'n': seqn, 'recv': time.time()}

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
                body = {'fieldID': fourcc, 'recv': {}, 'timestamp': time.time()}

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
                        body['recv'][field['key']] = (unpacked[i] * scale) + shift
                    else:
                        body['recv'][field['key']] = unpacked[i]

                # Debug
                yield body
            else:
                print "skipped unkown header", fourcc

            # truncate what we've already read
            packet = packet[message_length:]


class GPSMessages(object):
    """generage messages for GPS Const"""

    def __init__(self, messages):
        self.messages = messages

    def make_messages(self, data):
        body = {'fieldID': "SATS", 'recv': data, 'timestamp': time.time()}
        yield body


################################################################################
# FEED DEFS
################################################################################

# GPS Constilation
GPS = {
    'listener': GPSConst,
    'listener_args': {},
    'message_type': GPSMessages,
    'messages': {
        'SATS': {
            'members': [
                {'key': "Num_Sats"},
                {'key': "Sky"},
            ],
        },
    },
}


# Flight Computer
FC = {
    'listener': UDPListener,
    'listener_args': {'ip': "", 'port': 35001},
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
                {'key': "Magn_X",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.05}},
                {'key': "Magn_Y",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.05}},
                {'key': "Magn_Z",  'struct': "h", 'units': {'mks': "tesla", 'scale': 0.05}},
                {'key': "Temp",    'struct': "h", 'units': {'mks': "c", 'scale': 0.14 , 'shift': 25}},
                {'key': "Aux_ADC", 'struct': "h", 'units': {'mks': "volt", 'scale': 806}},
            ],
        },
        'ROLL': {
            'type': "Fixed",
            'endianness': '<',
            'members': [
                {'key': "PWM", 'struct': "H", 'units': {'mks': "seconds", 'scale': 1, 'shift': -1500}},
                {'key': "Disable", 'struct': "B"},
            ],
        },
        'RNHH': {
            'type': "Fixed",
            'endianness': '!',
            'members': [
                {'key': "Temperature", 'struct': "H", 'units': {'mks': "k", 'scale': .1}},
                {'key': "TS1Temperature", 'struct': "h", 'units': {'mks': "c", 'scale': .1}},
                {'key': "TS2Temperature", 'struct': "h", 'units': {'mks': "c", 'scale': .1}},
                {'key': "TempRange", 'struct': "H"},
                {'key': "Voltage", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
                {'key': "Current", 'struct': "h", 'units': {'mks': "amp", 'scale': .001}},
                {'key': "AverageCurrent", 'struct': "h", 'units': {'mks': "amp", 'scale': .001}},
                {'key': "CellVoltage1", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
                {'key': "CellVoltage2", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
                {'key': "CellVoltage3", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
                {'key': "CellVoltage4", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
                {'key': "PackVoltage", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
                {'key': "AverageVoltage", 'struct': "H", 'units': {'mks': "volt", 'scale': .001}},
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
                {'key': "Message"},
            ],
        },
        'GPS1': {
            'type': "Fixed",
            'endianness': '<',
            'members': [
                {'key': "AgeOfDiff",        'struct': "B", 'units': {'mks': "seconds"}},
                {'key': "NumOfSats",        'struct': "B"},
                {'key': "GPSWeek",          'struct': "H"},
                {'key': "GPSTimeOfWeek",    'struct': "d", 'units': {'mks': "seconds"}},
                {'key': "Latitude",         'struct': "d", 'units': {'mks': "degrees"}},
                {'key': "Longitude",        'struct': "d", 'units': {'mks': "degrees"}},
                {'key': "Height",           'struct': "f", 'units': {'mks': "meters"}},
                {'key': "VNorth",           'struct': "f", 'units': {'mks': "meter/s"}},
                {'key': "VEast",            'struct': "f", 'units': {'mks': "meter/s"}},
                {'key': "VUp",              'struct': "f", 'units': {'mks': "meter/s"}},
                {'key': "StdDevResid",      'struct': "f", 'units': {'mks': "meters"}},
                {'key': "NavMode",          'struct': "H"},
                {'key': "ExtendedAgeOfDiff",'struct': "H", 'units': {'mks': "seconds"}},
            ],
        },
    },
}

# List all active feeds
FEEDS = {
    'fc': FC,
    'gps': GPS,
}
