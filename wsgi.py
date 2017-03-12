import os
import cherrypy
import pymongo

import files


class application(object):
    m = None
    cursor = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'], int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    db = cursor.hitched
    invitations = db.invitations

    @cherrypy.expose
    def index(self):
        resource = open(os.path.join(files.get_root(), "index.html"), 'r')
        response_body = resource.read()
        return response_body

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return self.index()

    @cherrypy.expose
    def guest_address(self, address):
        guest = self.invitations.find_one({"addressLine1": address})
        return guest

    @cherrypy.expose
    def guest_name(self, name):
        guest = self.invitations.find_one({"First Name": name})
        return guest

