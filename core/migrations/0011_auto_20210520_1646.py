# Generated by Django 2.2.4 on 2021-05-20 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210520_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerstore',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]
