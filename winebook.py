import cgi
import os
import urllib
import logging
import datetime
import json
import re

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from ecdsa import SigningKey
from ecdsa.util import PRNG

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):

      template_values = {
              
      }

      template = JINJA_ENVIRONMENT.get_template('index.html')
      self.response.write(template.render(template_values))

class EnrollBottle(webapp2.RequestHandler):
  
  def post(self):
    bottle_name = '{0} {1} {2}'.format(self.request.get('vintage'), self.request.get('producer'), self.request.get('name') )
    
    logging.info( bottle_name )
    
    bottle_code = PRNG(bottle_name)
    
    rng1 = PRNG()
    sk1 = SigningKey.generate(entropy=rng1)
    vk1 = sk1.get_verifying_key()
    
    bottle_signature = sk.sign(bottle_code)
    assert vk.verify(bottle_signature, bottle_code)

    enclosure_code = PRNG(bottle_name)
    rng2 = PRNG()

    sk2 = SigningKey.generate(entropy=rng2)
    vk2 = sk2.get_verifying_key()
    
    enclosure_signature = sk.sign(enclosure_code)
    assert vk.verify(enclosure_signature, enclosure_code)
    
    bottle_label = (bottle_code, enclosure_signature)
    label = (vk1, vk2)
    enclosure_label = (bottle_signature, enclosure_code)
    
    logging.info('bottle label: {0}'.format(bottle_label))
    logging.info('label: {0}'.format(label))
    logging.info('enclosure label: {0}'.format(enclosure_label))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/enroll_bottle', EnrollBottle)
], debug=True)
