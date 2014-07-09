#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import config
import server
from feeds import FEEDS
from feeds import PacketListener
import Queue

# Make a Queue
q = Queue.Queue()

def run():

    # Spin up listener threads
    threads = []
    #for key, feed in FEEDS.iteritems():
    #    reader = feed['message_type'](feed['messages'])
    #    listener = feed['listener'](feed['listener_args'], reader)
    #    listener.add_queue(q)
    #    threads.append(listener)


    playtime = PacketListener(None)
    playtime.add_queue(q)
    threads.append(playtime)


    try:
        # Init tornado
        web = server.Webservice(q)

        for thread in threads:
            thread.start()

        # run tornado in main thread
        web.run()

    except KeyboardInterrupt, SystemExit:
        for thread in threads:
            thread.stop()


if __name__ == '__main__':
    run()
