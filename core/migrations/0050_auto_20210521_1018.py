# Generated by Django 2.2.4 on 2021-05-21 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_item_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='menu',
        ),
        migrations.AddField(
            model_name='menucategory',
            name='items',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Item'),
        ),
    ]
