# Generated by Django 3.1.7 on 2021-04-10 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solos', '0005_auto_20210410_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solo',
            name='album',
        ),
    ]
