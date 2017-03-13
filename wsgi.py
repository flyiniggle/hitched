import os
import cherrypy
from bson.json_util import dumps

import files

from lib.invitationservice import InvitationService
from lib.servererror import ServerError


class application(object):
    invitations_service = InvitationService()

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
        guest = self.invitations_service.get_invitation(address=address)

        if hasattr(guest, "error"):
            return dumps(ServerError("The record you were searching for could not be found."))
        else:
            return dumps(guest)

    @cherrypy.expose
    def guest_name(self, name):
        guest = self.invitations_service.get_invitation(name=name)

        if hasattr(guest, "error"):
            return dumps(ServerError("The record you were searching for could not be found."))
        else:
            return dumps(guest)

