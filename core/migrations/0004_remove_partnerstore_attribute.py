# Generated by Django 2.2.4 on 2021-05-19 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_dispatcher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partnerstore',
            name='attribute',
        ),
    ]