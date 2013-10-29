import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import config
import stats
import json
import os

clients = []


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


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
        self.pstat = stats.PacketStats()

    def flush(self):
        self.pstat.run()

        packed_data = []
        while not self.queue.empty():
            for x in self.queue.get():
                if x.get('fieldID') == 'SEQN':
                    self.pstat.packet(x.get('n'), x.get('recv'))
                else:
                    packed_data.append(x)

        now = time.time()
        obj = {
          'fieldID': 'Stats',
          'PacketsReceivedTotal': self.pstat.packets,
          'PacketsLostTotal': self.pstat.missed,
          'PacketsReceivedRecently': self.pstat.this_packets,
          'PacketsLostRecently': self.pstat.this_missed,
          'MostRecentTimestamp': now,
          'TimeLastPacketReceived': now - self.pstat.last_packet_recv,
          'PacketRate': self.pstat.this_packets/float(config.FLUSH_RATE) * 1000,
          'DropRate': self.pstat.this_droprate,
          'CurrentSeqn': self.pstat.seqn,
          'data': stats.filter(packed_data)
        }

        for client in clients:
            client.write_message(json.dumps(obj))
        
    def run(self):
        self.ioloop.start()
