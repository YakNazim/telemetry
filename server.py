import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import template
import sqlite3
import time
import config
import stats
import yaml
import json
import os
import glob

# Stores list of attached clients for the websocket
clients = []

class Tileset(object):

    def __init__(self, filename):
        self.filename = filename

    def get_tile(self, z, x, y):
        ymax = 1 << z
        y = ymax - y - 1
        row = self.query('''SELECT tile_data FROM tiles
                            WHERE zoom_level = %s
                            AND tile_column = %s
                            AND tile_row = %s''' % (z,x,y))
        if not row:
            return None
        return bytes(row[0])

    def query(self, sql):
        db = getattr(self, '_database', None)
        if db is None:
            self._database = self.connect()
            db = self._database
        
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row

    def connect(self):
        return sqlite3.connect(self.filename)


class MainHandler(tornado.web.RequestHandler):
    """Basic web server. This is a single page javascript webapp"""

    WidgetDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "frontend/widgets/")
    Template = template.Loader(WidgetDir)

    def get(self, profile=None):

        # Find all .yml files
        files_yml = glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/*.yml"))

        # Make lise of files + names
        Profiles = []
        for f in files_yml:
            with open(f, 'r') as y:
                p = yaml.load(y, Loader=yaml.Loader)
                Profiles.append({
                    'name': p['title'],
                    'slug': p['title'],
                    'uri': "/profiles/"+p['title'],
                    'file': f
                })

        #print Profiles

        if profile is not None:
            for p in Profiles:
                if p['slug'] == profile:
                    filename = p['file']
                    break
            else:
                filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/default.yml")
        else:
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles/default.yml")

        # Parse profile:
        # place to stash the rendered html inside of a widget
        rendered_widgets = []

        # Open fiel, loop, parse, render
        with open(filename, 'r') as y:
            profile = yaml.load(y, Loader=yaml.Loader)
            widgets = []
            for widget in profile['blocks']:
                title = widget['title']
                wtype = widget['type']
                html = self.Template.load(wtype+'.html').generate(name=title, metrics=widget)

                # store rendered html to inject in main page
                widget['html'] = html
                rendered_widgets.append(widget)

        # final call to render page with list of rendered contents
        self.render('index.html', layouts=Profiles, widgets=rendered_widgets)


class NewLayoutHandler(tornado.web.RequestHandler):
    """Basic web server that creates and saves new layouts"""

    def get(self):
        self.render('new.html')

class TileServer(tornado.web.RequestHandler):

    tilesets = {'brothers': Tileset('data/maps/brothers/mbtiles/brothers.mbtiles')}
    def get(self, **r):
        t = self.tilesets[r['mapname']].get_tile(int(r['z']), int(r['x']), int(r['y']))
        if t is None:
            t = ""
        self.write(t)
        self.set_header("Content-Type", "image/png")


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
                (r'/profiles/([^/]+)', MainHandler),
                (r'/maps/(?P<mapname>[^\/]+)/?(?P<z>[^\/]+)/?(?P<x>[^\/]+)?/?(?P<y>[^\/]+)?/', TileServer),
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
            for feed, data in self.queue.get().items():
                # debug
                #print data
                pstat.append_data(feed, data)

        # We're finished gathering data
        data = pstat.data

        data['servertime'] = time.time()

        # write data to clients
        for client in clients:
            client.write_message(json.dumps(data))

    def run(self):
        """Starts the IOloop. This is blocking!"""
        self.ioloop.start()
