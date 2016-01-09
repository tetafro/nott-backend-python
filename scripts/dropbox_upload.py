#!/usr/bin/python3

"""
Upload given file to Dropbox
TODO: get proper Dropbox token from pass.ini
"""

import dropbox
import sys, os

files = sys.argv[1:]
token = 'my-token'
client = dropbox.client.DropboxClient(token)

for file in files:
    f = open(file, 'rb')
    try:
        remote_file = os.path.basename(file)
        response = client.put_file(remote_file, f)
    except dropbox.rest.ErrorResponse as e:
        print(str(e))
    else:
        print('Uploaded succesfully')
