import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.ioloop import IOLoop
import socket
import os

class UDPStream(object):

    def __init__(self, socket, in_ioloop=None):
        self.socket = socket
        self._state = None
        self._read_callback = None
        self.ioloop = in_ioloop or IOLoop.instance()

    def _add_io_state(self, state):
        if self._state is None:
            self._state = tornado.ioloop.IOLoop.ERROR | state
            self.ioloop.add_handler(
                self.socket.fileno(), self._handle_events, self._state)
        elif not self._state & state:
            self._state = self._state | state
            self.ioloop.update_handler(self.socket.fileno(), self._state)

    def send(self):
        msg = "dorks"
        return self.socket.send(msg)

    def recv(self,sz):
        return self.socket.recv(sz)
    
    def close(self):
        self.ioloop.remove_handler(self.socket.fileno())
        self.socket.close()
        self.socket = None

    def read_chunk(self, callback=None, timeout=4):
        self._read_callback = callback
        self._read_timeout = self.ioloop.add_timeout( time.time() + timeout, 
            self.check_read_callback )
        self._add_io_state(self.ioloop.READ)

    def check_read_callback(self):
        if self._read_callback:
            # XXX close socket?
            self._read_callback(None, error='timeout');

    def _handle_read(self):
        if self._read_timeout:
            self.ioloop.remove_timeout(self._read_timeout)
        if self._read_callback:
            try:
                data = self.socket.recv(4096)
            except:
                # conn refused??
                data = None
            self._read_callback(data);
            self._read_callback = None

    def _handle_events(self, fd, events):
        if events & self.ioloop.READ:
            self._handle_read()
        if events & self.ioloop.ERROR:
            logging.error('%s event error' % self)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('client.html')


def connect():
    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsock.setblocking(False)
    udpsock.connect( ('127.0.0.1', 8080) )
    s = UDPStream(udpsock)

def thing(a):
    print "sock-",a#, type(sock)
    #sock.send('a')

#data = yield gen.Task( s.read_chunk )

def main():
    #s.send( 'some data' )


    static_path = os.path.join(os.path.dirname(__file__), 'static')

    application = tornado.web.Application([
            (r'/', MainHandler),
        ], template_path=static_path, static_path=static_path)
    application.listen(8088)


    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsock.setblocking(False)
    udpsock.connect( ('127.0.0.1', 8080) )
    s = UDPStream(udpsock)

    #sched = tornado.ioloop.PeriodicCallback(s.send, 1000, io_loop=tornado.ioloop.IOLoop.instance())
    #sched.start()


    #tornado.ioloop.IOLoop.instance().start()
    print 'running'

if __name__ == "__main__":
    static_path = os.path.join(os.path.dirname(__file__), 'static')

    application = tornado.web.Application([
            (r'/', MainHandler),
    ], template_path=static_path, static_path=static_path)
    application.listen(8088)


    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsock.setblocking(False)
    udpsock.connect( ('127.0.0.1', 8080) )

    #sched = tornado.ioloop.PeriodicCallback(s.send, 1000, io_loop=tornado.ioloop.IOLoop.instance())
    #sched.start()

    ioloop = tornado.ioloop.IOLoop.instance()

    def this():
        print "this"
    
    def connect():
        s = UDPStream(udpsock, ioloop)
        #data = yield gen.Task( s.read_chunk )
        data = yield tornado.gen.Task( s.read_chunk, this )

    connect()

    ioloop.start()
    print "running"
