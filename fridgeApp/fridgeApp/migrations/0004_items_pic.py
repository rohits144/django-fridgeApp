# Generated by Django 4.2.1 on 2023-05-27 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridgeApp', '0003_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='items_images'),
        ),
    ]