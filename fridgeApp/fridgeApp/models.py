from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

import logging

logger = logging.getLogger()


class Items(models.Model):
    """
    Table structure for each Item
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    expiry_date = models.DateField()
    pic = models.ImageField(upload_to="items_images", blank=True, null=True, default='abc.jpg')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def days_remaining(self):
        return self.expiry_date - datetime.date.today()


@receiver(post_save, sender=Items)
def update_image(sender, instance, created, **kwargs):
    if created and instance.pic == None:
        instance.pic = 'items_images/abc.jpg'
        instance.save()

