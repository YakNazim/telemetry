#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import config
import server
from feeds import FEEDS
import threading
import Queue

# Make a Queue
q = Queue.Queue()

# Init tornado
web = server.Webservice(q)

# Spin up listener threads
threads = []
for key, feed in FEEDS.iteritems():
    ip = feed['ip']
    port = feed['port']
    reader = feed['message_type'](feed['messages'])
    listener = feed['listener'](ip, port, reader)
    listener.add_queue(q)
    threads.append(listener)


# Start
try:
    for thread in threads:
        thread.start()

    # run tornado in main thread
    web.run()

except KeyboardInterrupt, SystemExit:
    for thread in threads:
        thread.stop()
    pass

