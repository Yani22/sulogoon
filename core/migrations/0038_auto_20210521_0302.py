# Generated by Django 2.2.4 on 2021-05-20 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20210521_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rider',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], max_length=15, null=True),
        ),
    ]
