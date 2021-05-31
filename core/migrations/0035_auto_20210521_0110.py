# Generated by Django 2.2.4 on 2021-05-20 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20210521_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='suffix',
            field=models.CharField(blank=True, choices=[('', 'None'), ('Sr', 'Sr.'), ('Jr', 'Jr.'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V'), ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'), ('XII', 'XII')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, null=True),
        ),
    ]