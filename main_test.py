import webapp2
import unittest
import webtest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main

class AppTest(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    # clear database between tests
    ndb.get_context().clear_cache()
    self.testapp = webtest.TestApp(main.app)

  def tearDown(self):
    self.testbed.deactivate()

  def testHelloWorldHandler(self):
    response = self.testapp.post('/profile', {
        'emailID': 'test@example.com',
        'firstName': 'testFirstName',
        'lastName': 'testLastName',
    })
    self.assertEqual(response.status_int, 200)

    response = self.testapp.get('/profile', {'userID': 'test@example.com'})
    self.assertEqual(response.status_int, 200)
    self.assertIn('email:  test@example.com', response.body)
    self.assertIn('First name:  testFirstName', response.body)
    self.assertIn('Last name:  testLastName', response.body)
