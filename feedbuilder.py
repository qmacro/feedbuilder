import os, cgi, logging, datetime
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Entry(db.Model):
  title = db.StringProperty()
  link = db.StringProperty()
  updated = db.DateTimeProperty(auto_now_add=True)
  summary = db.StringProperty(multiline=True)

class StartPage(webapp.RequestHandler):
  def get(self):
    self.redirect('/data/start.html')

class Feed(webapp.RequestHandler):
  def get(self):
    entry_query = Entry.all().order('-updated')
    entries = entry_query.fetch(15)

    template_values = {
      'now': datetime.datetime.now(),
      'feedname': 'Test feed',
      'feedlink': self.request.url,
      'feedid': 'test-feed-1',
      'entries': entries,
    }

    path = os.path.join(os.path.dirname(__file__), 'feed.xml')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    entry = Entry()
    entry.title = self.request.get('title')
    entry.link = self.request.get('link')
    entry.summary = self.request.get('summary')
    entry.put()
    self.redirect('/feed/')

class EntryForm(webapp.RequestHandler):
  def get(self):

    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'entryform.html')
    self.response.out.write(template.render(path, template_values))

class GotoAdmin(webapp.RequestHandler):
  def post(self):
    un = self.request.get('theusername')
    sc = self.request.get('secretcode')
    if (sc == "qwerty" and un == "Joseph") or (sc == "uiop" and un == "Dj"):
      self.redirect('/_ah/admin/')
    else:
      self.redirect('/data/start.html')


application = webapp.WSGIApplication(
  [
    ('/', StartPage),
    ('/feed/', Feed),
    ('/gotoadmin/', GotoAdmin),
    ('/entryform', EntryForm)
  ],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()





