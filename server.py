import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import config
import json
import os

clients = []


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('client.html')


class FrontEndWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        if self not in clients:
            clients.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        if self in clients:
            clients.remove(self)



class Webservice(object):

    def __init__(self, queue):
        static_path = os.path.join(os.path.dirname(__file__), 'static')
        self.application = tornado.web.Application([
                (r'/', MainHandler),
                (r'/ws', FrontEndWebSocket),
                (r'/(.*)', tornado.web.StaticFileHandler, dict(path=static_path)),
            ], template_path=static_path, static_path=static_path)
        self.queue = queue
        self.application.listen(config.APP_PORT)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        sched = tornado.ioloop.PeriodicCallback(self.flush, config.FLUSH_RATE, io_loop=self.ioloop)
        sched.start()
        self.packets = 0
        self.last_seqn = 0
        self.last_packet_recv = 0
        self.missed = 0

    def flush(self):
        packets = 0
        seqn = 0
        missed = 0
        while not self.queue.empty():
            for x in self.queue.get():
                if x.get('fieldID') == 'SEQN':
                    packets += 1
                    self.packets += 1
                    seqn = x.get('n')
                    missed = (seqn - self.last_seqn) - 1

                    self.last_seqn = seqn
                    self.last_packet_recv = x.get('recv')
                #for client in clients:
                #    client.write_message(json.dumps(x))

        self.missed += missed
        droprate = 0
        if packets:
            droprate = missed/float(packets+missed) * 100
        now = time.time()
        obj = {
          'fieldID': 'Stats',
          'PacketsReceivedTotal': self.packets,
          'PacketsLostTotal': self.missed,
          'PacketsReceivedRecently': packets,
          'PacketsLostRecently': missed,
          'MostRecentTimestamp': now,
          'TimeLastPacketReceived': now - self.last_packet_recv,
          'PacketRate': packets/float(config.FLUSH_RATE) * 1000,
          'DropRate': droprate,
        }

        for client in clients:
            client.write_message(json.dumps(obj))

    def run(self):
        self.ioloop.start()

"""        
class FrontEndWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):  # appends a new connection to the end of the array of
                     # connections and generates its position in the array
        open_web_sockets_lock.acquire()
        open_web_sockets.append(self)
        self.list_position = len(open_web_sockets) - 1
        open_web_sockets_lock.release()

    def on_message(self, message):
        pass

    def on_close(self):  # closes a connection in the array of connections by
                         # removing it from is position
        open_web_sockets_lock.acquire()
        open_web_sockets.pop(self.list_position)
        open_web_sockets_lock.release()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('client.html')

static_path = os.path.join(os.path.dirname(__file__), 'static')

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/ws', FrontEndWebSocket),
    (r'/(.*)', tornado.web.StaticFileHandler, dict(path=static_path)),
], template_path=static_path, static_path=static_path)


def tornado_thread(arg1, arg2):  # defines a thread that runs a Tornado IO loop
                                 # that listens to port 8080
    application.listen(8080)  # For some OS's and network setups, this line
                              # generates: "Error [10049]: The requested
                              # address is not valid in its context".
    tornado.ioloop.IOLoop.instance().start()


# Send JSON object to the front-end application
def send_json_obj(json_obj):
    if bool(json_obj) is False:
        return

    # To decode the JSON objects in Python, use:
    # objDecoded = json.loads(json_obj)
    # print objDecoded['fieldID'], objDecoded['timestamp']
    open_web_sockets_lock.acquire()

    for webSocket in open_web_sockets:  # iterates through every open
                                        # connections in the array
        if webSocket is None:  # if the connection is null
            print "It is none"

        tornado.ioloop.IOLoop.instance().add_callback(
            webSocket.write_message,
            json.dumps(json_obj)
        )  # creates a write event that will run during the next iteration
           # of the Tornado io loop. The event will send the json object
           # to the front end. For more detailed info, see:
           #   http://www.tornadoweb.org/en/stable/ioloop.html#callbacks-and-timeouts
           #   http://www.tornadoweb.org/en/stable/websocket.html?highlight=websockets#output
           #   http://docs.python.org/2/library/json.html#basic-usage

    open_web_sockets_lock.release()

"""
