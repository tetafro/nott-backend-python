from django.db import models


class Config(models.Model):
    """
    Application-wide settings that can be set by admins
    """

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=80)
    datatype = models.CharField(max_length=20)
    value = models.CharField(max_length=80)
