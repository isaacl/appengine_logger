import json
import logging

import webapp2

from google.appengine.ext import db

class DbStat(db.Model):
  created_date = db.DateTimeProperty(auto_now_add=True)
  client_id = db.StringProperty(required=True)
  data = db.TextProperty(required=True)

class Main(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Yo!')

    def post(self):
      raw_data = self.request.get('data')
      assert 0 < len(raw_data) < 10000
      data = json.loads(raw_data)
      client_id = data.get('client_id')
      assert isinstance(client_id, basestring) and 8 < len(client_id) < 40
      logging.info('Blob len %d, id "%s"' % (len(raw_data), client_id))
      DbStat(client_id=client_id, data=raw_data).put()


application = webapp2.WSGIApplication([
    ('/', Main),
], debug=True)
