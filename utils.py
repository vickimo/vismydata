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
    return_dict = {}
    headers = blob_reader_object.readline()
    headers = headers.strip().split(',')
    #TODO make this a list concatenation
    return_dict['data'] = [dict(zip(headers, str(x).strip().split(','))) for x in blob_reader_object]
    return_dict['metadata'] = ''
    return return_dict
    
