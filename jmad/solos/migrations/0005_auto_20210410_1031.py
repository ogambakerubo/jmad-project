# Generated by Django 3.1.7 on 2021-04-10 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
        ('solos', '0004_solo_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solo',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.track'),
        ),
    ]
