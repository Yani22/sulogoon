# Generated by Django 2.2.4 on 2021-05-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20210521_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatcher',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='rider',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, null=True),
        ),
    ]
