# Generated by Django 2.0.3 on 2018-04-13 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ffs', '0008_auto_20180412_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
