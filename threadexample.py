#!/usr/bin/env python
import time
import socket
import threading
import Queue
import os
import tornado.ioloop
import tornado.web

class ListenUDP(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self._stop = threading.Event()
        self.daemon = True

        UDP_IP = "127.0.0.1"
        UDP_PORT = 8080

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.sock.settimeout(0.1)

    def run(self):
        while (not self._stop.is_set()):
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                self.queue.put(data)
            except:
                pass

    def stop(self):
        self._stop.set()
        self.join()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('client.html')


class Messages(object):

    def __init__(self, queue):
        self.queue = queue

    def printer(self):
        while not self.queue.empty():
            print self.queue.get()

if __name__ == '__main__':
    q = Queue.Queue()
    stream = ListenUDP(q)
    mess = Messages(q)

    try:
        stream.start()
        static_path = os.path.join(os.path.dirname(__file__), 'static')

        application = tornado.web.Application([
            (r'/', MainHandler),
        ], template_path=static_path, static_path=static_path)
        application.listen(8088)

        ioloop = tornado.ioloop.IOLoop.instance()
        sched = tornado.ioloop.PeriodicCallback(mess.printer, 500, io_loop=ioloop)
        sched.start()
        ioloop.start()

    except KeyboardInterrupt, SystemExit:
        stream.stop()
        pass