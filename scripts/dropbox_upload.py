#!/usr/bin/python3

"""
Upload given file to Dropbox
TODO: get proper Dropbox token from pass.ini
"""

import sys, os
import dropbox

# Get token here: https://www.dropbox.com/developers/apps
TOKEN = os.environ.get('DROPBOX_TOKEN')

files = sys.argv[1:]
client = dropbox.Dropbox(TOKEN)

for file in files:
    with open(file, 'rb') as f:
        try:
            filename = os.path.basename(file)
            response = client.files_upload(f.read(), '/'+   filename)
        except Exception as e:
            print('Upload error: '+str(e))
        else:
            print('Uploaded succesfully')
