from django.contrib import admin
from main.models import User, Notepad, Note

admin.site.register(User)
admin.site.register(Notepad)
admin.site.register(Note)