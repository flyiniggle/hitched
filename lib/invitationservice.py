import os
import re
import pymongo
from exceptions import BaseException
from bson.objectid import ObjectId


class InvitationService(object):


    try:
        cursor = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'], int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
    except KeyError:
        cursor = pymongo.MongoClient(os.environ['MONGODB_URL'])

    db = cursor.hitched
    invitations = db.invitations

    def get_invitation(self, name="", address=""):
        if len(name) < 3 and len(address) < 4:
            raise InvitationServiceLookupError("Please refine your query.", 2)

        if name:
            query = {
                "$or": [
                    {"Name": {"$regex": '{}'.format(re.escape(name)), "$options": "-i"}},
                    {
                        "Guests.Name": {
                            "$regex": '{}'.format(re.escape(name)), "$options": "-i"
                        }
                    }
                ]
            }
        elif address:
            query = {"Address": {"$regex": '^{}'.format(re.escape(address)), "$options": "-i"}}
        else:
            raise InvitationServiceLookupError("No searchable attribute was found.", 1)
        guest = self.invitations.find(query, {"Guests": 1, "Plus One": 1, "Address": 1, "Name": 1})

        if guest.count() == 1:
            return guest[0]
        elif guest.count() > 1:
            return guest
        else:
            raise InvitationServiceLookupError("Search did not match any records.", 2)

    def update_invitation(self, invitationId, guests):
        for guest in guests:
            if guest.get("name", "") == "plusone":
                result = self.invitations.update_one(
                    {"_id": ObjectId(invitationId)},
                    {
                        "$addToSet": {
                            "Guests": {
                                "isComing": guest.get("isComing", False),
                                "isVegetarian": guest.get("isVegetarian", False),
                                "isCamping": guest.get("isCamping", False),
                                "displayName": guest.get("displayName", ""),
                                "Name": guest.get("displayName", "")
                            }
                        },
                        "$set": {
                            "Plus One": False
                        }
                    })
            else:
                result = self.invitations.update_one(
                    {"_id": ObjectId(invitationId), "Guests.Name": guest.get("name")},
                    {
                        "$set": {
                            "Guests.$.isComing": guest.get("isComing", False),
                            "Guests.$.isVegetarian": guest.get("isVegetarian", False),
                            "Guests.$.isCamping": guest.get("isCamping", False),
                            "Guests.$.displayName": guest.get("displayName", "")
                        }
                    })
            if result.matched_count != 1 or not bool(result.raw_result.get("updatedExisting")):
                raise InvitationServiceLookupError("Update did not match any records.", 2)

        return True


class InvitationServiceLookupError(BaseException):
    def __init__(self, message, code):
        super(InvitationServiceLookupError, self).__init__()
        self.error = str(message)
        self.errorCode = int(code)