import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import config
import stats
import json
import os

# Stores list of attached clients for the websocket
clients = []


class MainHandler(tornado.web.RequestHandler):
    """Basic web server. This is a single page javascript webapp"""

    def get(self):
        self.render('index.html')


class NewLayoutHandler(tornado.web.RequestHandler):
    """Basic web server that creates and saves new layouts"""

    def get(self):
        self.render('new.html')


class FrontEndWebSocket(tornado.websocket.WebSocketHandler):
    """Basic WebSocket class"""

    def open(self):
        if self not in clients:
            clients.append(self)

    def on_message(self, message):
        """We're throwing out messages from the front end"""
        pass

    def on_close(self):
        if self in clients:
            clients.remove(self)


class Webservice(object):
    """The webservice will spin up a webserver that listens on the configured port both for serving the
    static content and the data websocket
    """

    def __init__(self, queue):

        # Reference to thread queue
        self.queue = queue

        # Configure tornado HTTPServer
        static_path = os.path.join(os.path.dirname(__file__), 'static')
        template_path = os.path.join(os.path.dirname(__file__), 'frontend')
        self.application = tornado.web.Application([
                (r'/', MainHandler),
                (r'/create', NewLayoutHandler),
                (r'/ws', FrontEndWebSocket),
                (r'/(.*)', tornado.web.StaticFileHandler, dict(path=static_path)),
            ], template_path=template_path, static_path=static_path)
        self.application.listen(config.APP_PORT)

        self.ioloop = tornado.ioloop.IOLoop.instance()

        # Always be sending data to frontend, set up scheduled callbacks
        sched = tornado.ioloop.PeriodicCallback(self.flush, config.FLUSH_RATE, io_loop=self.ioloop)
        sched.start()

    def flush(self):
        """Called by tornado.ioloop.PeriodicCallback when we want the front end synced to
        current data that's been collected. Reads out the data and sends it to a statstics
        class the collates it.
        """

        # Make statitics object
        pstat = stats.PacketStats()

        # pull data out of queue (from listener threads)
        while not self.queue.empty():
            for data in self.queue.get():
                pstat.append_data(data)

        # We're finished gathering data
        data = pstat.data

        data['servertime'] = time.time()

        # write data to clients
        for client in clients:
            client.write_message(json.dumps(data))

    def run(self):
        """Starts the IOloop. This is blocking!"""
        self.ioloop.start()
