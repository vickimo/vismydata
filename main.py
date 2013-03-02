#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#imports (woo!)
#==============================================================================

import os
import time
import datetime
import urllib
import urllib2
import json
import random

import webapp2
import jinja2

from google.appengine.ext import db, blobstore
from google.appengine.ext.webapp import blobstore_handlers

#boilerplate (yay boilerplate!)
#==============================================================================

templateDir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templateDir),
                               autoescape = True)

#request handler helper class
#==============================================================================
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#models
#==============================================================================

#handlers
#==============================================================================
class IndexHandler(Handler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        blobs = blobstore.BlobInfo.all()
        self.render('index.html', upload_url=upload_url, blobs=blobs)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        self.redirect('/')

    def readContents(self, blob_reader):
        for line in blob_reader:
            line = line.split(',')
            

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

#redirects
#==============================================================================
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/upload', UploadHandler),
    ('/serve/([^/]+)?', ServeHandler)
], debug=True)

## Notes from SO.

# import os
# import urllib

# from google.appengine.ext import blobstore
# from google.appengine.ext import webapp
# from google.appengine.ext.webapp import blobstore_handlers
# from google.appengine.ext.webapp import template
# from google.appengine.ext.webapp.util import run_wsgi_app

# class MainHandler(webapp.RequestHandler):
#     def get(self):
#         upload_url = blobstore.create_upload_url('/upload')
#         self.response.out.write('<html><body>')
#         self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
#         self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

#         for b in blobstore.BlobInfo.all():
#             self.response.out.write('<li><a href="/serve/%s' % str(b.key()) + '">' + str(b.filename) + '</a>')

# class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
#     def post(self):
#         upload_files = self.get_uploads('file')
#         blob_info = upload_files[0]
#         self.redirect('/')

# class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
#     def get(self, blob_key):
#         blob_key = str(urllib.unquote(blob_key))
#         if not blobstore.get(blob_key):
#             self.error(404)
#         else:
#             self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)

# def main():
#     application = webapp.WSGIApplication(
#           [('/', MainHandler),
#            ('/upload', UploadHandler),
#            ('/serve/([^/]+)?', ServeHandler),
#           ], debug=True)
#     run_wsgi_app(application)

# if __name__ == '__main__':
#   main()
