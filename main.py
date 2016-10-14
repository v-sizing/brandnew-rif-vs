# Copyright 2016 Table Top Inventing
# All rights reserved.

import cgi
import urllib
import webapp2
from google.appengine.ext import ndb

class Profile(ndb.Model):
    emailID = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_profile(cls, user_key):
        return cls.query(ancestor=user_key)

class Clothing(ndb.Model):
    UPC= ndb.StringProperty()
    measurements = ndb.StringProperty()
    store = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_clothing(cls, user_key):
        return cls.query(ancestor=user_key)

# This class handles both the post AND get methods for Profiles
class manageProfile(webapp2.RequestHandler):
    def post(self):
        emailID = self.request.get('emailID')
        thisProfile = Profile(parent=ndb.Key("Profile",
                                           emailID or "*notitle*"),
                            emailID=self.request.get('emailID'),
                            firstName=self.request.get('firstName'),
                            lastName=self.request.get('lastName'))
        thisProfile.put()
    def get(self):
        self.response.out.write('<html><body>Your profile info.</br></br>')
        # The following requires a way to determine which profile (login, etc.)
        # currently use something like this:  http://localhost:8080/profile?userID=testcase@mail.com
        userID = self.request.get('userID')
        user_key = ndb.Key("Profile", userID)
        thatProfile = Profile.query_profile(user_key).get()
        self.response.out.write('email:  ' + thatProfile.emailID + '</br>')
        self.response.out.write('First name:  ' + thatProfile.firstName + '</br>')
        self.response.out.write('Last name:  ' + thatProfile.lastName + '</br>')
        self.response.out.write('</html></body>')

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