import os
import re
import pymongo


class InvitationService(object):
    cursor = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'], int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    db = cursor.hitched
    invitations = db.invitations

    def get_invitation(self, name="", address=""):
        if name:
            query = {"Name": {"$regex": '^{}$'.format(re.escape(name)), "$options": "-i"}}
        elif address:
            query = {"Address": {"$regex": '^{}$'.format(re.escape(address)), "$options": "-i"}}
        else:
            return InvitationServiceLookupError("No searchable attribute was found.", 1)
        guest = self.invitations.find(query, {"_id": 0, "Guests": 1, "Plus One": 1, "Address": 1})

        if guest.count() == 1:
            return guest[0]
        elif guest.count() > 1:
            return guest
        else:
            return InvitationServiceLookupError("Search did not match any records", 2)


class InvitationServiceLookupError(object):
    def __init__(self, message, code):
        super(InvitationServiceLookupError, self).__init__()
        self.error = str(message)
        self.errorCode = int(code)