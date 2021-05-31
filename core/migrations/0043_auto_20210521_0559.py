# Generated by Django 2.2.4 on 2021-05-20 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20210521_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='menu_category',
        ),
        migrations.RemoveField(
            model_name='menucategory',
            name='user',
        ),
        migrations.AddField(
            model_name='menucategory',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Item'),
        ),
    ]
