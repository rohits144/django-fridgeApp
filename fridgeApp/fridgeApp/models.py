from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime


import logging
logger = logging.getLogger()


class Items(models.Model):
    """
    Table structure for each Item
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    expiry_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name