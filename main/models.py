from django.db import models

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    avatar = models.CharField(max_length=128)
    reg_date = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)