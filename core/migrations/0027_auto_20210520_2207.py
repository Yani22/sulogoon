# Generated by Django 2.2.4 on 2021-05-20 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210520_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='contact',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]