import cgi
import os
import urllib
import logging
import datetime
import json
import binascii

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from ecdsa.ecdsa import SigningKey
from ecdsa.ecdsa import *
from ecdsa.ecdsa.curves import NIST384p

from ecdsa.ecdsa.util import PRNG
from base58 import base58

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''

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
    
    bottle_code = PRNG(datetime.datetime.now().microsecond)(128)

    rng1 = PRNG(datetime.datetime.now().microsecond)
    sk1 = SigningKey.generate(curve=NIST384p, entropy=rng1)
    vk1 = sk1.get_verifying_key()
    
    bottle_signature = sk1.sign(bottle_code)
    assert vk1.verify(bottle_signature, bottle_code)
    
    enclosure_code = PRNG(datetime.datetime.now().microsecond)(128)
    rng2 = PRNG(datetime.datetime.now().microsecond)

    sk2 = SigningKey.generate(curve=NIST384p, entropy=rng2)
    vk2 = sk2.get_verifying_key()
    
    enclosure_signature = sk2.sign(enclosure_code)
    assert vk2.verify(enclosure_signature, enclosure_code)
    
    bottle_tuple = {'bottle_code' : base58.b58encode( bottle_code ), 'enclosure_signature' : base58.b58encode( enclosure_signature )}
    label_tuple = { 'bottle_key' : { 'x' : vk1.pubkey.point.x(), 'y' : vk1.pubkey.point.y() }, 'enclosure_key' : base58.b58encode( vk2.to_string()) }
    enclosure_tuple = { 'bottle_signature' : base58.b58encode( bottle_signature ), 'enclosure_code' : base58.b58encode( enclosure_code) }
    
    logging.info('bottle code: {0}'.format(bottle_tuple))
    logging.info (binascii.hexlify(bottle_code))
    
    logging.info('label code: {0}'.format(label_tuple))
    logging.info('enclosure code: {0}'.format(enclosure_tuple))

    logging.info( vk1.pubkey.curve )
    logging.info ( vk1.pubkey.point.x() )
    logging.info ( vk1.pubkey.point.y() )
    
    response_json = {'bottle_tuple':bottle_tuple, 'label_tuple':label_tuple, 'enclosure_tuple':enclosure_tuple}
    
    self.response.write( json.dumps(response_json) )

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/enroll_bottle', EnrollBottle)
], debug=True)

