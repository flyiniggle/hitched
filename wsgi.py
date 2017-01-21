import os
import cherrypy

import files


class application(object):
    m = None

    @cherrypy.expose
    def index(self):
        resource = open(os.path.join(files.get_root(), "index.html"), 'r')
        response_body = resource.read()
        return response_body

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return self.index()
