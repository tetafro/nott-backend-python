"""
Export all data from database to single text file.
"""

import os
import sys
import re
from datetime import datetime

import django


# Django setup
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(
    os.path.join(SCRIPTS_DIR, '..', 'project')
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Django models
from apps.notes.models import Folder


now = datetime.now()
filename = 'export_%s.txt' % now.strftime('%Y%m%d')
export_file = open(filename, 'w')

regexps = [
    {
        'exp': re.compile(r'<p>(.*?)</p>'),
        'sub': r'\1\n'
    },
    {
        'exp': re.compile(r'(<font.*?>|</font>)'),
        'sub': r''
    },
    {
        'exp': re.compile(r'(<span.*?>|</span>)'),
        'sub': r''
    },
    {
        'exp': re.compile(r'(<strong.*?>|</strong>)'),
        'sub': r''
    },
    {
        'exp': re.compile(r'(<b>|</b>)'),
        'sub': r''
    },
    {
        'exp': re.compile(r'<br>'),
        'sub': r'\n'
    },
    {
        'exp': re.compile(r'&nbsp;'),
        'sub': r' '
    },
    {
        'exp': re.compile(r'&gt;'),
        'sub': r'>'
    },
    {
        'exp': re.compile(r'&lt;'),
        'sub': r'<'
    },
    {
        'exp': re.compile(r'&amp;'),
        'sub': r'&'
    }
]

all_folders = Folder.objects.all().order_by('title')
for folder in all_folders:
    export_file.write('-------------------------------\n')
    export_file.write('-------------------------------\n')
    export_file.write('-------------------------------\n')
    export_file.write('FOLDER: '+folder.title.upper()+'\n')
    export_file.write('-------------------------------\n')
    export_file.write('-------------------------------\n')
    export_file.write('-------------------------------\n\n')
    for notepad in folder.notepads.all().order_by('title'):
        export_file.write('-------------------------------\n')
        export_file.write('-------------------------------\n')
        export_file.write('NOTEPAD: '+notepad.title+'\n')
        export_file.write('-------------------------------\n')
        export_file.write('-------------------------------\n\n')
        for note in notepad.notes.all().order_by('title'):
            export_file.write('-------------------------------\n')
            export_file.write('NOTE: '+note.title+'\n')
            export_file.write('-------------------------------\n\n')

            text = note.text
            for r in regexps:
                text = r['exp'].sub(r['sub'], text)
            export_file.write(text)
