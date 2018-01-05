from django.db import models

from core.api import Serializer


class Setting(models.Model, Serializer):
    """Application-wide settings"""

    # Fields to be given to clients
    dict_fields = ['id', 'code', 'name', 'datatype', 'value']

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=80)
    datatype = models.CharField(max_length=20)
    value = models.CharField(max_length=80)
