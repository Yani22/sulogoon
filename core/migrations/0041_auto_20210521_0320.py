# Generated by Django 2.2.4 on 2021-05-20 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20210521_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rider',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='rider',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True),
        ),
    ]