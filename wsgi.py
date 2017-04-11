import os
import cherrypy
from bson.json_util import dumps
from json import loads
import urlparse
from ast import literal_eval

import files

from lib.invitationservice import InvitationService, InvitationServiceLookupError
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
        guest = self.invitations_service.get_invitation(address=urlparse.unquote(str(address)))

        if hasattr(guest, "error"):
            return dumps(ServerError("The record you were searching for could not be found."))
        else:
            return dumps(guest)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def rsvp(self, invitationId="", guests=""):
        try:
            self.invitations_service.update_invitation(invitationId, loads(guests))
            return dumps({"ok": True})
        except InvitationServiceLookupError:
            return dumps(ServerError("I'm sorry, we couldn't save your RSVP right now."))

    @cherrypy.expose
    def guest_name(self, name):
        guest = self.invitations_service.get_invitation(name=urlparse.unquote(str(name)))

        if hasattr(guest, "error"):
            return dumps(ServerError("The record you were searching for could not be found."))
        else:
            return dumps(guest)
