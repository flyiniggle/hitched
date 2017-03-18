import os
import pymongo


class InvitationService(object):
    cursor = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'], int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    db = cursor.hitched
    invitations = db.invitations

    def get_invitation(self, name="", address=""):
        if name:
            query = {"First Name": name}
        elif address:
            query = {"Address": address}
        else:
            return InvitationServiceLookupError("No searchable attribute was found.", 1)
        guest = self.invitations.find(query)

        if guest.count() != 1:
            return InvitationServiceLookupError("Search did not match exactly 1 record", 2)
        else:
            return guest


class InvitationServiceLookupError(object):
    def __init__(self, message, code):
        super(InvitationServiceLookupError, self).__init__()
        self.error = str(message)
        self.errorCode = int(code)