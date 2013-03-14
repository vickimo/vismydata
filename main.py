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

import utils

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
class Patron(db.Model):
    patron_name = db.TextProperty()
    joined_date = db.DateTimeProperty(auto_now_add = True)

class DataSeries(db.Model):
    blob_key = db.TextProperty()
    json_data = db.BlobProperty()
    name = db.TextProperty()

#handlers
#==============================================================================
class IndexHandler(Handler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        blobs = blobstore.BlobInfo.all()
        blob_infos = []
        for blob in blobs:
            blob_infos.append({'filename': blob.filename,
                               'key': str(blob.key())
                               })
        self.render('index.html', upload_url=upload_url, blobs=blob_infos)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.write('Chugging away...')
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        blob_reader = blobstore.BlobReader(str(blob_info.key()))
        row_dict = utils.readBlobCsv(blob_reader)
        ds = DataSeries(blob_key=str(blob_info.key()),
                        json_data=json.dumps(row_dict),
                        name=blob_info.filename)
        ds.put()
        self.redirect('/')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class PlotHandler(Handler):
    def get(self, blob_key):
        blob_reader = blobstore.BlobReader(blob_key)
        parsed = utils.readBlobCsv(blob_reader)
        self.write(parsed)

class DataHandler(Handler):
    def get(self, blob_key):
        blob_reader = blobstore.BlobReader(blob_key)
        row_dict = utils.readBlobCsv(blob_reader)
        self.write(json.dumps(row_dict))

#redirects
#==============================================================================
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/upload', UploadHandler),
    ('/serve/([^/]+)?', ServeHandler),
    ('/plot/([^/]+)?', PlotHandler),
    ('/load/([^/]+)?', DataHandler)
], debug=True)
