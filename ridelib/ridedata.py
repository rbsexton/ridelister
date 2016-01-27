'''The Google system uses python objects as database things'''
__all__ = (
    "RideDataItem",
)

from google.appengine.ext import ndb

class RideDataItem(ndb.Model):

    version = ndb.IntegerProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    
    name        = ndb.StringProperty()
    startdate   = ndb.DateProperty()
    description = ndb.StringProperty()

    leader  = ndb.StringProperty()

    startlocation = ndb.StringProperty()
    startcoords = ndb.GeoPtProperty()

    approved = ndb.BooleanProperty()

