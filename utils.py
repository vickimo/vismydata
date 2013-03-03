#!/usr/bin/env python
#This is a little file of helper functions.

from google.appengine.ext import db, blobstore

def readBlobCsv(blob_reader_object, headers=1):
    """
    This function will take in a blob reader object and output a dictionary
    with the following entries:
    - metadata
    - data
      - This is a list of dictionaries, with header:value pairs for each row.
    """
    all_rows = {}
    headers = blob_reader_object.readline()
    headers = headers.strip().split(',')
    #TODO make this a list concatenation
    all_rows['data'] = [dict(zip(headers, str(x).strip().split(','))) for x in blob_reader_object]
    all_rows['metadata'] = ''
    return all_rows
    
