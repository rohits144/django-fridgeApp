from django.db import models
from django.contrib.auth.models import User, Group


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


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(
        max_length=40, blank=True, null=True, default="/static/dpp.jpg")

    display_pic = models.ImageField(
        upload_to='profiles', verbose_name='profile picture', blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username