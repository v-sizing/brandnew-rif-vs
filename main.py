# Copyright 2016 Table Top Inventing
# All rights reserved.

import cgi
import json
import urllib
import webapp2
from google.appengine.ext import ndb


class measurePair(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.FloatProperty()

class userMorphology(ndb.Model):
    emailID = ndb.StringProperty()
    mPairs = ndb.StructuredProperty(measurePair, repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    @classmethod
    def query_morph(cls, user_key):
        return cls.query(ancestor=user_key)

class Profile(ndb.Model):
    emailID = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    userMeasurements = ndb.JsonProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    @classmethod
    def query_profile(cls, user_key):
        return cls.query(ancestor=user_key)

# This class handles both the post AND get methods for Profiles
class manageProfile(webapp2.RequestHandler):
    def post(self):
        # This section needed to parse the userMeasurements section of the post body
        j = json.loads(self.request.body)
        uM = j['userMeasurements']  # this is a list of dict objectts
        uPair = [measurePair(**item) for item in uM]  # this steps through the dictionary items from the dictionary list (uM), then it unpacks the dictionary item into measured pair, but it works because the input is assumed to have the form [{"name": "waistCircumference", "value": 32},{"name": "neckCircumference", "value": 16}]
        userMorph = userMorphology(parent = ndb.Key("Profile", j['emailID'] or "*notitle*"),
            emailID = j['emailID'], mPairs = uPair)

#        userMorph.mPairs = uPair    # hand uPair list of objects to the mPairs (repeated = True) structure container
        print "Morpho:  ", userMorph.mPairs
        userMorph.put()

        thisProfile = Profile(parent=ndb.Key("Profile",
                                           j['emailID'] or "*notitle*"),
                            emailID=j['emailID'],
                            firstName=j['firstName'],
                            lastName=j['lastName'])
        thisProfile.put()

    def get(self):
        self.response.out.write('<html><body>Your profile info.</br></br>')
        # The following requires a way to determine which profile (login, etc.)
        # currently use something like this:  http://localhost:8080/profile?userID=testcase@mail.com
        userID = self.request.get('userID')
        user_key = ndb.Key("Profile", userID)
        morph_key = ndb.Key("Profile", userID)
        thatProfile = Profile.query_profile(user_key).get()
        thatMorph = userMorphology.query_morph(morph_key).get()
        self.response.out.write('email:  ' + thatProfile.emailID + '</br>')
        self.response.out.write('First name:  ' + thatProfile.firstName + '</br>')
        self.response.out.write('Last name:  ' + thatProfile.lastName + '</br>')
        self.response.out.write('Pairs:  ' + thatMorph.emailID + '</br>')
        self.response.out.write('</html></body>')

class Clothing(ndb.Model):
    UPC= ndb.StringProperty()
    measurements = ndb.StringProperty()
    store = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_clothing(cls, user_key):
        return cls.query(ancestor=user_key)

# This class handles both the post AND get methods for Clothing
class manageClothing(webapp2.RequestHandler):
    def post(self):
        UPC = self.request.get('UPC')
        thisClothing = Clothing(parent=ndb.Key("Clothing",
                                           UPC or "*notitle*"),
                            UPC=self.request.get('UPC'),
                            measurements=self.request.get('measurements'),
                            store=self.request.get('store'))
        thisClothing.put()
    def get(self):
    	self.response.write('<html><body>Your clothing info.</br></br>')
        clothingID = self.request.get('clothingID')
        # currently use something like this:  http://localhost:8080/profile?clothingID=639382-00039
        clothing_key = ndb.Key("Clothing", clothingID)
        thatClothing = Clothing.query_clothing(clothing_key).get()
        self.response.out.write('UPC code:  ' + thatClothing.UPC + '</br>')
        self.response.out.write('Mesurements:  ' + thatClothing.measurements + '</br>')
        self.response.out.write('Store:  ' + thatClothing.store + '</br>')
        self.response.out.write('</html></body>')

app = webapp2.WSGIApplication([
    ('/profile', manageProfile),
    ('/clothing', manageClothing),
], debug=True)