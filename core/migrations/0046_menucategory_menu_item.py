# Generated by Django 2.2.4 on 2021-05-20 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20210521_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucategory',
            name='menu_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Item'),
        ),
    ]
