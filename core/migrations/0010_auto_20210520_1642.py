# Generated by Django 2.2.4 on 2021-05-20 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_attribute_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='title',
            new_name='name',
        ),
    ]
