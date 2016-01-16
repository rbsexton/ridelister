'''The Google system uses python objects as database things'''
__all__ = (
	"RideDataItem",
)

from google.appengine.ext import ndb

class RideDataItem(ndb.Model):
	name  = ndb.StringProperty()
	leader  = ndb.StringProperty()
	startlocation = ndb.StringProperty()
 	description = ndb.StringProperty()

