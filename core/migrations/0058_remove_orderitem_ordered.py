# Generated by Django 2.2.4 on 2021-05-27 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_itemcategory_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ordered',
        ),
    ]