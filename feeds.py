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
from psas_packet import io, messages


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


class PacketListener(Listener):
    """Use PSAS Packet"""

    def __init__(self, logfile):
        super(PacketListener, self).__init__(None)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 35001))
        #self.sock.settimeout(1)
        self.net = io.Network(self.sock, logfile=logfile)

    def thread(self):
        data = None
        data = []
        for d in self.net.listen():
            timestamp, values = d
            fourcc, values = values
            data.append({fourcc: dict({'recv': timestamp}, **values)})

        if len(data) > 0:
            for q in self.queues:
                q.put({'FC': data})


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


class GPSMessages(object):
    """generage messages for GPS Const"""

    def __init__(self, messages):
        self.messages = messages

    def make_messages(self, data):
        body = {'fieldID': "SATS", 'recv': data, 'timestamp': time.time()}
        yield body
